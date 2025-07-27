import os
import shutil
import logging

from openai import OpenAI, OpenAIError
from pydub import AudioSegment
from utils import valid_file_type
from faster_whisper import WhisperModel
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Transcriber():
  def __init__(self, api_key:str, provider:str, model_size:str):
    self.provider = None
    
    if provider == 'OpenAI':
      self.provider = CloudTranscriber(api_key)  
    else:
      self.provider = LocalTranscriber(model_size)
      
  def transcribe(self, audio_file_path) -> str:
    return self.provider.transcribe(audio_file_path=audio_file_path)

class LocalTranscriber():
  def __init__(self, model_size:str="tiny"):
    self.MODEL_SIZE = model_size
    self.model = WhisperModel(self.MODEL_SIZE, 'cpu', compute_type="int8")  
    
  def __transcribe_audio_file(self, audio_file_path):
    segments, _ = self.model.transcribe(audio_file_path, beam_size=5)
    segments = list(segments)
    return segments
  
  def transcribe(self, audio_file_path) -> str:
    if not os.path.exists(audio_file_path) or not os.path.isfile(audio_file_path):
      raise FileNotFoundError(f"Error: The file '{audio_file_path}' does not exist or is not a valid file.")

    if not valid_file_type(audio_file_path):
      raise ValueError(f"Only audio files accepted. '{audio_file_path}' is not an audio file.")

    try:
      start = time.perf_counter()
      segments = self.__transcribe_audio_file(audio_file_path)
      end = time.perf_counter()
      
      transcription = ''
      
      with open("transcription.txt", "w") as file:
        for segment in segments:
          transcription += segment.text
      return transcription
    except Exception as e:
      logging.error(f"An error occurred during transcription: {e}")
      raise RuntimeError(f"An error occurred during transcription: {e}")
    
class CloudTranscriber():
  MAX_CHUNK_LENGTH_IN_MS = 10 * 60 * 1000
  OUTPUT_CHUNKS_FOLDER_PATH = "output_chunks"
  
  def __init__(self, api_key):
    self.openai_client = OpenAI(api_key=api_key)
    if self.openai_client.api_key is None:
      raise OpenAIError("OpenAI API key is missing. Set it using OPENAI_API_KEY environment variable.")
    
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

  def __transcribe_multiple_chunks(self, chunk_file_paths):
    logging.info(f"Starting transcription of {len(chunk_file_paths)} chunks...")
    transcript = ""

    for i, chunk_file_path in enumerate(chunk_file_paths):
        transcript += self.__transcribe_audio_file(chunk_file_path)
        logging.info(f"Finished transcribing chunk {i + 1}/{len(chunk_file_paths)}")

    logging.info("Completed transcription of all chunks.")
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

  def transcribe(self, audio_file_path) -> str:
    if not os.path.exists(audio_file_path) or not os.path.isfile(audio_file_path):
      raise FileNotFoundError(f"Error: The file '{audio_file_path}' does not exist or is not a valid file.")

    if not valid_file_type(audio_file_path):
      raise ValueError(f"Only audio files accepted. '{audio_file_path}' is not an audio file.")

    try:
      logging.info(f"Loading audio file: {audio_file_path}")
      audio = AudioSegment.from_mp3(audio_file_path)

      if len(audio) <= self.MAX_CHUNK_LENGTH_IN_MS:
        return self.__transcribe_single_chunk(audio_file_path)
      else:
        audio_chunks = self.__split_audio(audio)
        chunk_file_paths = self.__generate_chunk_files(audio_chunks)
        transcript = self.__transcribe_multiple_chunks(chunk_file_paths)
        self.__delete_chunks()
        return transcript
    except Exception as e:
      logging.error(f"An error occurred during transcription: {e}")
      raise RuntimeError(f"An error occurred during transcription: {e}")