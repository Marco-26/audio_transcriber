import os
from openai import OpenAI
from pydub import AudioSegment
import shutil
import argparse
from transcriber import Transcriber

def save_transcript(transcript, filename):
  with open(filename, "w", encoding="utf-8") as output_file:
      output_file.write(transcript)

  print(f"Transcript saved to {filename}")

def main(args):
  audio_file_path = args.audio_file_path
  transcribed_file_name = args.transcribed_file_name
  
  if not os.path.exists(audio_file_path):
    print("Error: File not found.")
    return

  if not os.path.isfile(audio_file_path):
    print("Error: Provided audio path is not a file.")
    return

  if not transcribed_file_name.isalnum():
    print("Error: Filename should contain only alphanumeric characters.")
    return

  audio = AudioSegment.from_mp3(audio_file_path)
  transcriber = Transcriber(os.getenv("OPENAI_API_KEY"))
  transcript = transcriber.transcribe(audio,audio_file_path)
  print("Transcript: " + transcript)
  if transcript is not None:
    save_transcript(transcript, transcribed_file_name+".txt")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("audio_file_path", type=str, help="Path to the audio file to transcribe")
  parser.add_argument("transcribed_file_name", type=str, help="File name of transcribed audio")
  
  args = parser.parse_args()
  main(args)