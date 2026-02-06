from abc import ABC, abstractmethod

class BaseTranscriber(ABC):
    """Abstract base class defining the interface for all transcriber implementations."""
    
    @abstractmethod
    def transcribe(self, audio_file_path: str) -> str:
        """Transcribe audio file and return text.
        
        Args:
            audio_file_path: Path to the audio file to transcribe
            
        Returns:
            Transcribed text as a string
        """
        pass
