import logging
from base_transcriber import BaseTranscriber
from utils import validate_path
from constants import ModelSize
from faster_whisper import WhisperModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LocalTranscriber(BaseTranscriber):
  def __init__(self, model_size:ModelSize=ModelSize.TINY):
    self.model = WhisperModel(model_size.value, 'cpu', compute_type="int8")  
    
  def __transcribe_audio_file(self, audio_file_path, language=None):
    transcribe_params = {"beam_size": 5}
    if language:
      transcribe_params["language"] = language
    
    segments, _ = self.model.transcribe(audio_file_path, **transcribe_params)
    segments = list(segments)
    return segments
  
  def transcribe(self, audio_file_path, language=None) -> str:
    validate_path(audio_file_path)

    try:
      if language:
        logging.info(f"Using specified language: {language}")
      else:
        logging.info("Auto-detecting language...")
      
      segments = self.__transcribe_audio_file(audio_file_path, language)
      
      transcription = [""]
      
      with open("transcription.txt", "w") as file:
        for segment in segments:
          transcription.append(segment.text)
      return "".join(transcription)
    except Exception as e:
      logging.error(f"An error occurred during transcription: {e}")
      raise RuntimeError(f"An error occurred during transcription: {e}")
