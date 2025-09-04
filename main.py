import os
import argparse

from transcriber import Transcriber, MODEL_SIZES
from dotenv import load_dotenv
load_dotenv()

from utils import save_transcript
from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("audio", type=str, help='Filepath of audio file to use as raw audio source')
parser.add_argument("--provider", type=str, help='Type of provider to transcribe file (OpenAI, Local)', default='OpenAI', choices=["openai", "local"])
parser.add_argument("--model_size", type=str, help='Transcription Model Size', default='tiny', choices=MODEL_SIZES)

def main(args):
  audio_file_path = args.audio
  
  if not os.path.exists(audio_file_path):
    print("Error: File not found.")
    return

  if not os.path.isfile(audio_file_path):
    print("Error: Provided audio path is not a file.")
    return

  try:
    transcriber = Transcriber(os.getenv("OPENAI_API_KEY"), args.provider, args.model_size)
    transcript = transcriber.transcribe(audio_file_path)
    print(transcript)
    save_transcript(transcript=transcript)
  except FileNotFoundError as e:
    print(e)
  except ValueError as e:
    print(e)
  except RuntimeError as e:
    print(e)

if __name__ == "__main__":
  args = parser.parse_args()
  main(args)