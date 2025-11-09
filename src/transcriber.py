import os
import shutil
import logging
from openai import OpenAI
from pydub import AudioSegment
from utils import validate_path
from constants import MODEL_SIZES, MODEL_TYPES, WORKER_THREAD_COUNT
from faster_whisper import WhisperModel
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Transcriber():
  def __init__(self, api_key:str, provider:str, model_size:str):
    if provider.lower() == 'openai':
      self.provider = CloudTranscriber(api_key)  
    elif provider.lower() == 'local':
      self.provider = LocalTranscriber(model_size)
    else:
      raise ValueError(f"Provider {provider} not availabe. Providers: {MODEL_TYPES}")
  
  def transcribe(self, audio_file_path) -> str:
    if self.provider:
     return self.provider.transcribe(audio_file_path=audio_file_path)
     
    return ""

class LocalTranscriber():
  def __init__(self, model_size:str="tiny"):
    if model_size not in MODEL_SIZES:
      logging.error("Specified model size doesn't exist")
      raise ValueError(f'Invalid model size {model_size}. Available sizes: {MODEL_SIZES}')
        
    self.model = WhisperModel(model_size, 'cpu', compute_type="int8")  
    
  def __transcribe_audio_file(self, audio_file_path):
    segments, _ = self.model.transcribe(audio_file_path, beam_size=5)
    segments = list(segments)
    return segments
  
  def transcribe(self, audio_file_path) -> str:
    validate_path(audio_file_path)

    try:
      segments = self.__transcribe_audio_file(audio_file_path)
      
      transcription = [""]
      
      with open("transcription.txt", "w") as file:
        for segment in segments:
          transcription.append(segment.text)
      return "".join(transcription)
    except Exception as e:
      logging.error(f"An error occurred during transcription: {e}")
      raise RuntimeError(f"An error occurred during transcription: {e}")
    
class CloudTranscriber():
  MAX_CHUNK_LENGTH_IN_MS = 10 * 60 * 1000
  OUTPUT_CHUNKS_FOLDER_PATH = "output_chunks"
  
  def __init__(self, api_key):
    if not api_key:
      raise ValueError(f"API key not defined for OpenAI. Please set it using OPENAI_API_KEY environment variable.")
    
    self.openai_client = OpenAI(api_key=api_key)
    
  def __transcribe_audio_file(self, audio_file_path):
    with open(audio_file_path, "rb") as audio_to_transcribe:
      transcript_obj = self.openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_to_transcribe,
      )

    return transcript_obj.text

  def __transcribe_single_chunk(self, audio_chunk):
    logging.info("Starting transcription of single chunk...")
    transcript = self.__transcribe_audio_file(audio_chunk)
    logging.info("Finished transcribing single chunk.")
    return transcript

  def __split_audio(self, audio):
    logging.info("Splitting audio into smaller chunks...")
    audio_chunks = [audio[i:i + self.MAX_CHUNK_LENGTH_IN_MS] for i in range(0, len(audio), self.MAX_CHUNK_LENGTH_IN_MS)]
    logging.info(f"Audio split into {len(audio_chunks)} chunks.")
    return audio_chunks

  def __generate_chunk_files(self, audio_chunks):
    logging.info("Generating temporary chunk files...")
    chunk_file_paths = []

    if not os.path.exists(self.OUTPUT_CHUNKS_FOLDER_PATH):
      os.makedirs(self.OUTPUT_CHUNKS_FOLDER_PATH)

    for i, audio_chunk in enumerate(audio_chunks):
      chunk_file_path = os.path.join(self.OUTPUT_CHUNKS_FOLDER_PATH, f"chunk_{i}.mp3")
      audio_chunk.export(chunk_file_path, format="mp3")
      chunk_file_paths.append(chunk_file_path)

    logging.info(f"Created {len(chunk_file_paths)} chunk files from the original audio.")
    return chunk_file_paths

  def __delete_chunks(self):
    logging.info("Deleting temporary chunk files...")
    shutil.rmtree(self.OUTPUT_CHUNKS_FOLDER_PATH)
    os.makedirs(self.OUTPUT_CHUNKS_FOLDER_PATH)
    logging.info("Temporary chunk files deleted.")

  def __threading_transcription(self, chunk_file_paths) -> str:
    if not chunk_file_paths:
      raise ValueError("No chunk file paths provided for transcription.")

    results = [""] * len(chunk_file_paths)
    max_workers = min(WORKER_THREAD_COUNT, len(chunk_file_paths))
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
      results = list(pool.map(self.__transcribe_single_chunk, chunk_file_paths))
      
    return "".join(results)
    
  def transcribe(self, audio_file_path) -> str:
    validate_path(audio_file_path)

    try:
      logging.info(f"Loading audio file: {audio_file_path}")
      audio = AudioSegment.from_mp3(audio_file_path)

      if len(audio) <= self.MAX_CHUNK_LENGTH_IN_MS:
        return self.__transcribe_single_chunk(audio_file_path)
      else:
        audio_chunks = self.__split_audio(audio)
        chunk_file_paths = self.__generate_chunk_files(audio_chunks)
        
        transcript = self.__threading_transcription(chunk_file_paths=chunk_file_paths)
        self.__delete_chunks()
        return transcript
    except Exception as e:
      logging.error(f"An error occurred during transcription: {e}")
      raise RuntimeError(f"An error occurred during transcription: {e}")