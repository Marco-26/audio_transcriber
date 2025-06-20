import os
from openai import OpenAI, OpenAIError
import shutil
import argparse
from transcriber import Transcriber
from utils import save_transcript

parser = argparse.ArgumentParser()
parser.add_argument("audio", type=str, help='Filepath of audio file to use as raw audio source')
  
def main(args):
  audio_file_path = args.audio
  
  if not os.path.exists(audio_file_path):
    print("Error: File not found.")
    return

  if not os.path.isfile(audio_file_path):
    print("Error: Provided audio path is not a file.")
    return

  try:
    transcriber = Transcriber(os.getenv("OPENAI_API_KEY"))
    transcript = transcriber.transcribe(audio_file_path)
    save_transcript(transcript)
  except FileNotFoundError as e:
    print(e)
  except ValueError as e:
    print(e)
  except RuntimeError as e:
    print(e)

if __name__ == "__main__":
  args = parser.parse_args()
  main(args)