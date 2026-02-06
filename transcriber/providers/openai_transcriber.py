import os
import shutil
import logging
from openai import OpenAI
from pydub import AudioSegment
from transcriber.transcriber import BaseTranscriber 
from transcriber.utils import validate_path
from transcriber.constants import MAX_CONCURRENT_TRANSCRIPTIONS, LOG_TAG_OPENAI
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class OpenAITranscriber(BaseTranscriber):
  MAX_CHUNK_LENGTH_IN_MS = 10 * 60 * 1000
  OUTPUT_CHUNKS_FOLDER_PATH = "output_chunks"
  
  def __init__(self, api_key):
    if not api_key:
      raise ValueError(f"API key not defined for OpenAI. Please set it using OPENAI_API_KEY environment variable.")
    
    self.openai_client = OpenAI(api_key=api_key)
    
  def __transcribe_audio_file(self, audio_file_path, language=None):
    with open(audio_file_path, "rb") as audio_to_transcribe:
      params = {
        "model": "whisper-1",
        "file": audio_to_transcribe,
      }
      if language:
        params["language"] = language
      
      transcript_obj = self.openai_client.audio.transcriptions.create(**params)

    return transcript_obj.text

  def __transcribe_single_chunk(self, audio_chunk, language=None):
    logging.info(f"{LOG_TAG_OPENAI} Starting transcription of single chunk...")
    transcript = self.__transcribe_audio_file(audio_chunk, language)
    logging.info(f"{LOG_TAG_OPENAI} Finished transcribing single chunk.")
    return transcript

  def __split_audio(self, audio):
    logging.info(f"{LOG_TAG_OPENAI} Splitting audio into smaller chunks...")
    audio_chunks = [audio[i:i + self.MAX_CHUNK_LENGTH_IN_MS] for i in range(0, len(audio), self.MAX_CHUNK_LENGTH_IN_MS)]
    logging.info(f"{LOG_TAG_OPENAI} Audio split into {len(audio_chunks)} chunks.")
    return audio_chunks

  def __generate_chunk_files(self, audio_chunks):
    logging.info(f"{LOG_TAG_OPENAI} Generating temporary chunk files...")
    chunk_file_paths = []

    if not os.path.exists(self.OUTPUT_CHUNKS_FOLDER_PATH):
      os.makedirs(self.OUTPUT_CHUNKS_FOLDER_PATH)

    for i, audio_chunk in enumerate(audio_chunks):
      chunk_file_path = os.path.join(self.OUTPUT_CHUNKS_FOLDER_PATH, f"chunk_{i}.mp3")
      audio_chunk.export(chunk_file_path, format="mp3")
      chunk_file_paths.append(chunk_file_path)

    logging.info(f"{LOG_TAG_OPENAI} Created {len(chunk_file_paths)} chunk files from the original audio.")
    return chunk_file_paths

  def __delete_chunks(self):
    logging.info(f"{LOG_TAG_OPENAI} Deleting temporary chunk files...")
    shutil.rmtree(self.OUTPUT_CHUNKS_FOLDER_PATH)
    os.makedirs(self.OUTPUT_CHUNKS_FOLDER_PATH)
    logging.info(f"{LOG_TAG_OPENAI} Temporary chunk files deleted.")

  def __threading_transcription(self, chunk_file_paths, language=None) -> str:
    if not chunk_file_paths:
      raise ValueError("No chunk file paths provided for transcription.")

    results = [""] * len(chunk_file_paths)
    max_workers = min(MAX_CONCURRENT_TRANSCRIPTIONS, len(chunk_file_paths))
    logging.info(f"{LOG_TAG_OPENAI} Processing {len(chunk_file_paths)} chunks with {max_workers} concurrent workers...")
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
      results = list(pool.map(lambda chunk: self.__transcribe_single_chunk(chunk, language), chunk_file_paths))
      
    return "".join(results)
    
  def transcribe(self, audio_file_path, language=None) -> str:
    validate_path(audio_file_path)

    try:
      logging.info(f"{LOG_TAG_OPENAI} Loading audio file: {audio_file_path}")
      if language:
        logging.info(f"{LOG_TAG_OPENAI} Using specified language: {language}")
      else:
        logging.info(f"{LOG_TAG_OPENAI} Auto-detecting language...")
      
      audio = AudioSegment.from_mp3(audio_file_path)

      if len(audio) <= self.MAX_CHUNK_LENGTH_IN_MS:
        return self.__transcribe_single_chunk(audio_file_path, language)
      else:
        audio_chunks = self.__split_audio(audio)
        chunk_file_paths = self.__generate_chunk_files(audio_chunks)
        
        transcript = self.__threading_transcription(chunk_file_paths=chunk_file_paths, language=language)
        self.__delete_chunks()
        return transcript
    except Exception as e:
      logging.error(f"{LOG_TAG_OPENAI} An error occurred during transcription: {e}")
      raise RuntimeError(f"An error occurred during transcription: {e}")
