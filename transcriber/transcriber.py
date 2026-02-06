import logging
from constants import ModelSize, Provider
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BaseTranscriber(ABC):
  """Abstract base class defining the interface for all transcriber implementations."""
  
  @abstractmethod
  def transcribe(self, audio_file_path: str, language: str = None) -> str:
    """Transcribe audio file and return text.
    
    Args:
        audio_file_path: Path to the audio file to transcribe
        language: Optional ISO 639-1 language code (e.g., 'en', 'es', 'fr'). 
                  If None, language will be auto-detected.
        
    Returns:
        Transcribed text as a string
    """
    pass

class TranscriberFactory:
  @staticmethod
  def create(api_key: str, provider: Provider, model_size: ModelSize):
    if provider == Provider.OPENAI:
      from providers.openai_transcriber import OpenAITranscriber
      return OpenAITranscriber(api_key)
    elif provider == Provider.LOCAL:
      from providers.local_transcriber import LocalTranscriber
      return LocalTranscriber(model_size)
    elif provider == Provider.DEEPGRAM:
      from providers.deepgram_transcriber import DeepgramTranscriber
      return DeepgramTranscriber(api_key)

class Transcriber(BaseTranscriber):
  def __init__(self, api_key:str, provider:Provider, model_size:ModelSize):
    self.provider = TranscriberFactory.create(api_key, provider, model_size)
  
  def transcribe(self, audio_file_path, language=None) -> str:
    return self.provider.transcribe(audio_file_path=audio_file_path, language=language)