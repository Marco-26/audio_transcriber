import os
from openai import OpenAI
from pydub import AudioSegment
import shutil

MAX_CHUNK_LENGTH_IN_MS = 10 * 60 * 1000
OUTPUT_CHUNKS_FOLDER_PATH = "output_chunks"

def transcribe_audio_file(openai_client, audio_file_path):
    with open(audio_file_path, "rb") as audio_to_transcribe:
        transcript_obj = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_to_transcribe,

        )

    return transcript_obj.text

def transcribe_single_chunk(openai_client, audio_chunk):
    print("Starting transcription")
    transcript = transcribe_audio_file(openai_client, audio_chunk)
    print(f"Finished transcribing audio")
    return transcript

def transcribe_multiple_chunks(openai_client, chunk_file_paths):
    print("Starting transcription")

    transcript = ""

    for i, chunk_file_path in enumerate(chunk_file_paths):
        transcript += transcribe_audio_file(openai_client, chunk_file_path)
        print(f"Finished transcribing chunk {i}")

    print("Finished transcription")

    return transcript

def split_audio(audio):
    print("Splitting audio into smaller chunks")
    audio_chunks = [audio[i:i+MAX_CHUNK_LENGTH_IN_MS] for i in range(0, len(audio), MAX_CHUNK_LENGTH_IN_MS)]
    print("Done splitting the audio...")
    return audio_chunks

def generate_chunk_files(audio_chunks):
    print("Generating temporary chunk files...")
    chunk_file_paths = []
    
    if not os.path.exists(OUTPUT_CHUNKS_FOLDER_PATH):
        os.makedirs(OUTPUT_CHUNKS_FOLDER_PATH)

    for i, audio_chunk in enumerate(audio_chunks):
        chunk_file_path = os.path.join(OUTPUT_CHUNKS_FOLDER_PATH, f"chunk_{i}.mp3")
        audio_chunk.export(chunk_file_path, format="mp3")
        chunk_file_paths.append(chunk_file_path)

    print(f"Created {len(chunk_file_paths)} chunks from the original audio")

    return chunk_file_paths

def save_transcript(transcript, filename):
    with open(filename, "w", encoding="utf-8") as output_file:
        output_file.write(transcript)

    print(f"Transcript saved to {filename}")

def delete_chunks():
    shutil.rmtree(OUTPUT_CHUNKS_FOLDER_PATH)
    os.makedirs(OUTPUT_CHUNKS_FOLDER_PATH)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: {} <audio_file_path> <transcribed_file_name>".format(sys.argv[0]))
        sys.exit(1)

    audio_file_path = sys.argv[1]
    transcribed_file_name = sys.argv[2]

    if not os.path.exists(audio_file_path):
        print("Error: File not found.")
        sys.exit(1)

    if not os.path.isfile(audio_file_path):
        print("Error: Provided audio path is not a file.")
        sys.exit(1)

    if not transcribed_file_name.isalnum():
        print("Error: Filename should contain only alphanumeric characters.")
        sys.exit(1)

    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    audio = AudioSegment.from_mp3(audio_file_path)

    try:
        if len(audio) <= MAX_CHUNK_LENGTH_IN_MS:
            transcript = transcribe_single_chunk(openai_client, audio_file_path)
        else:
            audio_chunks = split_audio(audio)
            chunk_file_paths = generate_chunk_files(audio_chunks)

            transcript = transcribe_multiple_chunks(openai_client, chunk_file_paths)
            delete_chunks()
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        sys.exit(1)

    save_transcript(transcript, transcribed_file_name+".txt")