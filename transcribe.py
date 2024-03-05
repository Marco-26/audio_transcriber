import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file):
  with open(file, "rb") as audio_to_transcribe:
      transcript = client.audio.transcriptions.create(
          model="whisper-1", 
          file=audio_to_transcribe,
      )
  return transcript.text;

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: {} <audio_file_path>".format(sys.argv[0]))
        sys.exit(1)

    audio_file_path = sys.argv[1]
    if not os.path.isfile(audio_file_path):
        print("Error: File not found.")
        sys.exit(1)

    transcript = transcribe_audio(audio_file_path)
    print(transcript)