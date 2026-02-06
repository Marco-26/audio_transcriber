import logging
from constants import ModelSize, Provider
from transcriber_factory import TranscriberFactory

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Transcriber():
  def __init__(self, api_key:str, provider:Provider, model_size:ModelSize):
    self.provider = TranscriberFactory.create(api_key, provider, model_size)
  
  def transcribe(self, audio_file_path, language=None) -> str:
    if self.provider:
     return self.provider.transcribe(audio_file_path=audio_file_path, language=language)

    return ""