import os
from openai import OpenAI
from pydub import AudioSegment

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file):
  with open(file, "rb") as audio_to_transcribe:
      transcript = client.audio.transcriptions.create(
          model="whisper-1", 
          file=audio_to_transcribe,
      )
  return transcript.text;

def split_audio(file):
    audio = AudioSegment.from_mp3(file)
    one_minute = 10 * 60 * 2500
    first_minute = audio[:one_minute]
    first_minute.export("first_minute.mp3", format="mp3")

if __name__ == "__main__":
    import sys

    # i f len(sys.argv) != 2:
    #     print("Usage:7 {} <audio_file_path>".format(sys.argv[0]))
    #     sys.exit(1)

    audio_file_path = "first_minute.mp3" 

    if not os.path.isfile(audio_file_path):
        print("Error: File not found.")
        sys.exit(1)
    
    #split_audio(audio_file_path)

    transcript = transcribe_audio(audio_file_path)
    print(transcript)