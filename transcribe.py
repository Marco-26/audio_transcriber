import os
from openai import OpenAI
from pydub import AudioSegment

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#TODO: Implement a inbuilt audio compressor
def transcribe_single_chunk(chunk):
    print("Starting transcription")
    transcripted_chunk = ""

    try: 
        with open(chunk, "rb") as audio_to_transcribe:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_to_transcribe,
        )
        print(f"Finished transcribing audio/s")
        transcripted_chunk = transcript.text
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        sys.exit(1)

    return transcripted_chunk

def transcribe_multiple_chunks(chunk_files):
    num_chunks = len(chunk_files)
    print("Starting transcription")

    transcripted_chunks = ""
    
    for i in range(num_chunks):
        try:
            with open(chunk_files[i], "rb") as audio_to_transcribe:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_to_transcribe,
            )
            print(f"Finished transcribing {i} chunks/s")
            transcripted_chunks += transcript.text
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            sys.exit(1)

    print("Finished transcription")

    return transcripted_chunks;

def split_audio(file_path):
    print("Splitting audio into smaller chunks")
    audio = AudioSegment.from_mp3(file_path)
    max_chunk_length = 25 
    chunks = []

    total_duration = len(audio) / 1000 
    duration_minutes = total_duration / 60

    num_chunks = round(duration_minutes / max_chunk_length)
    chunk_duration = total_duration / num_chunks

    start_time = 0
    for i in range(num_chunks):
        end_time = start_time + chunk_duration
        chunk = audio[int(start_time * 1000):int(end_time * 1000)]
        chunks.append(chunk)
        start_time = end_time

    print("Done splitting the audio...")

    return chunks

def generate_chunk_files(chunks):
    print("Generating temporary chunk files...")
    chunk_files = []

    for i, chunk in enumerate(chunks):
        temp_file_path = os.path.join("output_chunks", f"chunk_{i}.mp3")
        chunk.export(temp_file_path, format="mp3")
        chunk_files.append(temp_file_path)
    
    print(f"Created {len(chunk_files)} chunks from the original audio")

    return chunk_files

def get_file_size(audio_file_path):
    audio = AudioSegment.from_mp3(audio_file_path)
    total_duration = len(audio) / 1000 
    duration_minutes = total_duration / 60
    
    return duration_minutes

def save_transcript(transcript, filename):
    with open(filename+".txt", "w") as output_file:
        output_file.write(transcript)

    print(f"Transcript saved to {filename}")

def prompt_file_name():
    while True:
        file_name = input("Enter the desired filename to save the transcript (without extension): ")
        if not file_name:
            print("Error: Filename cannot be empty.")
            continue
        elif not file_name.isalnum():
            print("Error: Filename should contain only alphanumeric characters.")
            continue
        else:
            break
    return file_name

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage:7 {} <audio_file_path>".format(sys.argv[0]))
        sys.exit(1)
    
    print("It's highly recommended to compress the audio before using this script...")

    file_name = prompt_file_name()
    audio_file_path = sys.argv[1]
    
    if not os.path.isfile(audio_file_path):
        print("Error: File not found.")
        sys.exit(1)

    if(get_file_size(audio_file_path) <=25):
        transcript = transcribe_single_chunk(audio_file_path)
    else:
        chunks = split_audio(audio_file_path)
        chunk_files = generate_chunk_files(chunks)

        transcript = transcribe_multiple_chunks(chunk_files)
    
    save_transcript(transcript,file_name)