import logging
import argparse
import os

from transcriber import Transcriber, MODEL_SIZES

from utils import save_transcript
from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("audio", type=str, help='Filepath of audio file to use as raw audio source')
parser.add_argument("--provider", type=str, help='Type of provider to transcribe file (OpenAI, Local)', default='OpenAI', choices=["openai", "local"])
parser.add_argument("--model_size", type=str, help='Transcription Model Size', default='tiny', choices=MODEL_SIZES)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main(args):
  try:
    transcriber = Transcriber(os.getenv("OPENAI_API_KEY"), args.provider, args.model_size)
    transcript = transcriber.transcribe(args.audio)
    if transcript:
      save_transcript(transcript=transcript)
  except FileNotFoundError as e:
    logging.error(e)
  except ValueError as e:
    logging.error(e)
  except RuntimeError as e:
    logging.error(e)

if __name__ == "__main__":
  args = parser.parse_args()
  main(args)