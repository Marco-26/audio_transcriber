import os
import shutil

from openai import OpenAI


class Transcriber:
  MAX_CHUNK_LENGTH_IN_MS = 10 * 60 * 1000
  OUTPUT_CHUNKS_FOLDER_PATH = "output_chunks"

  def __init__(self, api_key):
    self.openai_client = OpenAI(api_key=api_key)
  
  def transcribe_audio_file(self, audio_file_path):
    with open(audio_file_path, "rb") as audio_to_transcribe:
        transcript_obj = self.openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_to_transcribe,
        )

    return transcript_obj.text

  def transcribe_single_chunk(self, audio_chunk):
    print("Starting transcription")
    transcript = self.transcribe_audio_file(audio_chunk)
    print(f"Finished transcribing audio")
    return transcript

  def transcribe_multiple_chunks(self, chunk_file_paths):
    print("Starting transcription")

    transcript = ""

    for i, chunk_file_path in enumerate(chunk_file_paths):
        transcript += self.transcribe_audio_file(chunk_file_path)
        print(f"Finished transcribing chunk {i}")

    print("Finished transcription")

    return transcript

  def split_audio(self,audio):
    print("Splitting audio into smaller chunks")
    audio_chunks = [audio[i:i+self.MAX_CHUNK_LENGTH_IN_MS] for i in range(0, len(audio), self.MAX_CHUNK_LENGTH_IN_MS)]
    print("Done splitting the audio...")
    return audio_chunks

  def generate_chunk_files(self,audio_chunks):
    print("Generating temporary chunk files...")
    chunk_file_paths = []
    
    if not os.path.exists(self.OUTPUT_CHUNKS_FOLDER_PATH):
        os.makedirs(self.OUTPUT_CHUNKS_FOLDER_PATH)

    for i, audio_chunk in enumerate(audio_chunks):
        chunk_file_path = os.path.join(self.OUTPUT_CHUNKS_FOLDER_PATH, f"chunk_{i}.mp3")
        audio_chunk.export(chunk_file_path, format="mp3")
        chunk_file_paths.append(chunk_file_path)

    print(f"Created {len(chunk_file_paths)} chunks from the original audio")

    return chunk_file_paths

  def delete_chunks(self):
    shutil.rmtree(self.OUTPUT_CHUNKS_FOLDER_PATH)
    os.makedirs(self.OUTPUT_CHUNKS_FOLDER_PATH)
    
  def transcribe(self, audio, audio_file_path):
    try:
      if len(audio) <= self.MAX_CHUNK_LENGTH_IN_MS:
        transcript = self.transcribe_single_chunk(audio_file_path)
      else:
        audio_chunks = self.split_audio(audio)
        chunk_file_paths = self.generate_chunk_files(audio_chunks)

        transcript = self.transcribe_multiple_chunks(chunk_file_paths)
        self.delete_chunks()
      return transcript
    except Exception as e:
      print(f"An error occurred during transcription: {e}")
      return None