import pathlib
import logging

def valid_file_type(filename:str):
  accepted_types = ['.mp3', '.mp4', '.wav']
  file_extension = pathlib.Path(filename).suffix.lower()
  if file_extension in accepted_types:
    return True
  else:
    return False
  
def save_transcript(transcript):
  with open("transcript.txt", "w", encoding="utf-8") as output_file:
      output_file.write(transcript)

  logging.info("Transcript saved to transcript.txt")