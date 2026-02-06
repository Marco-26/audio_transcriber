from abc import ABC, abstractmethod

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
