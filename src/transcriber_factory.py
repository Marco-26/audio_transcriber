import logging
from constants import ModelSize, Provider

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TranscriberFactory:
    """Factory class for creating transcriber instances based on provider type."""
    
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
        else:
            raise ValueError(f"Invalid provider: {provider}. Available providers: {list(Provider)}")
