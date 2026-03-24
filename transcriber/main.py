import logging
import argparse
from transcriber import Transcriber
from utils import save_transcript
from constants import OPENAI_API_KEY, DEEPGRAM_API_KEY, ModelSize, Provider, LOG_TAG_MAIN

parser = argparse.ArgumentParser()
parser.add_argument("audio", type=str, help='Filepath of audio file to use as raw audio source')
parser.add_argument("--provider", type=Provider, help='Type of provider to transcribe file (OpenAI, Local, Deepgram)', default=Provider.OPENAI, choices=list(Provider))
parser.add_argument("--model_size", type=ModelSize, help='Transcription Model Size', default=ModelSize.TINY, choices=list(ModelSize))
parser.add_argument("--language", type=str, help='ISO 639-1 language code (e.g., en, es, fr). If not specified, language will be auto-detected.', default=None)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main(args):
  try:
    if args.provider == Provider.OPENAI:
      api_key = OPENAI_API_KEY
    elif args.provider == Provider.DEEPGRAM:
      api_key = DEEPGRAM_API_KEY
    else:
      api_key = None
    
    transcriber = Transcriber(api_key, Provider(args.provider), ModelSize(args.model_size))
    transcript = transcriber.transcribe(args.audio, language=args.language)
    
    if not transcript:
      logging.warning(f"{LOG_TAG_MAIN} Transcript is null...")
      return
    
    save_transcript(transcript=transcript)
  except FileNotFoundError as e:
    logging.error(f"{LOG_TAG_MAIN} {e}")
  except ValueError as e:
    logging.error(f"{LOG_TAG_MAIN} {e}")
  except RuntimeError as e:
    logging.error(f"{LOG_TAG_MAIN} {e}")

if __name__ == "__main__":
  args = parser.parse_args()
  main(args)