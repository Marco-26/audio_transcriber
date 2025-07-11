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

class Transcriber:
  MAX_CHUNK_LENGTH_IN_MS = 10 * 60 * 1000
  OUTPUT_CHUNKS_FOLDER_PATH = "output_chunks"
  MODEL_SIZE = "tiny"
  
  def __init__(self, api_key):
    self.model = WhisperModel(self.MODEL_SIZE, 'cpu', compute_type="int8")  
    
  def __transcribe_audio_file(self, audio_file_path):
    segments, _ = self.model.transcribe(audio_file_path, beam_size=5)
    segments = list(segments)
    return segments

  def transcribe(self, audio_file_path):
    if not os.path.exists(audio_file_path) or not os.path.isfile(audio_file_path):
      raise FileNotFoundError(f"Error: The file '{audio_file_path}' does not exist or is not a valid file.")

    if not valid_file_type(audio_file_path):
      raise ValueError(f"Only audio files accepted. '{audio_file_path}' is not an audio file.")

    try:
      start = time.perf_counter()
      segments = self.__transcribe_audio_file(audio_file_path)
      end = time.perf_counter()
      
      with open("transcription.txt", "w") as file:
        for segment in segments:
          file.write(segment.text)
          
      print(f"Transcription took: {(end-start):.2f} seconds. Saved to transcription.txt")
    except Exception as e:
      logging.error(f"An error occurred during transcription: {e}")
      raise RuntimeError(f"An error occurred during transcription: {e}")