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

# def split_audio(file):
#     output_folder = "output_chunks"
#     max_chunk_size_min = 25

#     audio = AudioSegment.from_mp3(file)
#     duration_seconds = len(audio) / 1000
#     duration_minutes = duration_seconds / 60

#     #quantity of chunks needed
#     n = round(duration_minutes / max_chunk_size_min)

#     print("Length: " + str(duration_minutes))
#     print("Chunks needed: " + str(n))

#     for x in n:
def split_audio(file_path, num_chunks):
    audio = AudioSegment.from_mp3(file_path)

    # Calculate the duration of each chunk
    total_duration = len(audio) / 1000  # Convert milliseconds to seconds
    chunk_duration = total_duration / num_chunks

    # Split the audio into chunks
    chunks = []
    start_time = 0
    for i in range(num_chunks):
        end_time = start_time + chunk_duration
        chunk = audio[int(start_time * 1000):int(end_time * 1000)]
        chunks.append(chunk)
        start_time = end_time

    return chunks

if __name__ == "__main__":
    import sys

    # i f len(sys.argv) != 2:
    #     print("Usage:7 {} <audio_file_path>".format(sys.argv[0]))
    #     sys.exit(1)

    audio_file_path = "20240229.mp3" 

    if not os.path.isfile(audio_file_path):
        print("Error: File not found.")
        sys.exit(1)
    
    chunks = split_audio(audio_file_path, 7)
    print(chunks)

    for i, chunk in enumerate(chunks):
        chunk.export(f"output_chunk_{i + 1}.mp3", format="mp3", parameters=["-ac", "2", "-ar", "44100", "-ab", "192k"])

    # transcript = transcribe_audio(audio_file_path)
    # print(transcript)