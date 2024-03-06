import os
from openai import OpenAI
from pydub import AudioSegment

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(chunk_files):
    num_chunks = len(chunk_files)
    if num_chunks == 0:
        return

    print("Starting transcription")

    
    with open(chunk_files[0], "rb") as audio_to_transcribe:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_to_transcribe,
    )
        
    print("Finished transcription")

    return transcript.text;

def split_audio(file_path):
    print("Splitting audio into smaller chunks")
    audio = AudioSegment.from_mp3(file_path)
    max_chunk_length = 25

    total_duration = len(audio) / 1000 
    duration_minutes = total_duration / 60
    
    num_chunks = round(duration_minutes / max_chunk_length)
    chunk_duration = total_duration / num_chunks

    chunks = []
    start_time = 0
    for i in range(num_chunks):
        end_time = start_time + chunk_duration
        chunk = audio[int(start_time * 1000):int(end_time * 1000)]
        chunks.append(chunk)
        start_time = end_time

    print("Done splitting the audio...")
    print(f"Created {num_chunks} chunks from the original audio")

    return chunks

def generate_chunk_files(chunks):
    print("Generating temporary chunk files...")
    chunk_files = []

    for i, chunk in enumerate(chunks):
        temp_file_path = os.path.join("output_chunks", f"chunk_{i}.mp3")
        chunk.export(temp_file_path, format="mp3")
        chunk_files.append(temp_file_path)

    return chunk_files

if __name__ == "__main__":
    import sys

    # i f len(sys.argv) != 2:
    #     print("Usage:7 {} <audio_file_path>".format(sys.argv[0]))
    #     sys.exit(1)

    audio_file_path = "20240229.mp3" 

    if not os.path.isfile(audio_file_path):
        print("Error: File not found.")
        sys.exit(1)
    
    chunks = split_audio(audio_file_path)
    chunk_files = generate_chunk_files(chunks)

    transcript = transcribe_audio(chunk_files)
    print(transcript)