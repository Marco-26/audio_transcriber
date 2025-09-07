import pathlib
import logging
import magic

from pathlib import Path
  
def save_transcript(transcript):
  with open("transcript.txt", "w", encoding="utf-8") as output_file:
      output_file.write(transcript)

  logging.info("Transcript saved to transcript.txt")
  
def validate_path(audio_file_path):  
  if not Path(audio_file_path).exists() or not Path(audio_file_path).is_file():
    raise FileNotFoundError(f"The file '{audio_file_path}' does not exist or is not a file.")

  mime = magic.from_file(audio_file_path, mime=True)
  print(mime)
  if mime != 'audio/mpeg':
    raise ValueError(f"Only audio files are allowed")