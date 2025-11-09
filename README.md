# Audio Transcription Tool

This Python tool transcribes audio files using either the OpenAI API or a local Whisper model. It can split large audio files into smaller chunks, transcribe each chunk, and combine the results into a single text file.

## Prerequisites

Before using this tool, make sure you have the following installed:

- [Python 3.7+](https://www.python.org/)
- [FFmpeg](https://ffmpeg.org/)
- An OpenAI API key set as an environment variable named `OPENAI_API_KEY` (required for OpenAI provider)

To install all dependencies, first create a virtual environment:

```bash
git clone https://github.com/Marco-26/audio-transcriber.git
cd audio-transcriber/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Note:** You must manually install ffmpeg (e.g., `brew install ffmpeg` on macOS).

## Usage

Run the tool with:

```bash
python main.py <audio_file_path> [--provider PROVIDER] [--model_size MODEL_SIZE]
```

- `<audio_file_path>`: Path to the audio file you want to transcribe (required).
- `--provider`: Type of provider to use for transcription. Options: `OpenAI` (default), `Local` (runs the Whisper model directly on your machine using local CPU/GPU resources).
- `--model_size`: (For local provider) Whisper model size. Default: `tiny`.

**Example:**

```bash
python main.py data/example_audio.mp3
python main.py data/example_audio.mp3 --provider Local --model_size small
```

The transcript will be saved to a file named `transcript.txt` in the project root folder.

## Features

- Audio Splitting: Large audio files are automatically split into smaller chunks for efficient transcription.
- Transcription: Transcribes audio files using either the OpenAI API or a local Whisper model.
- Output: Saves the transcript as a text file.
- Provider Selection: Choose between OpenAI cloud or local transcription.

## Recommendations

- **Audio Compression:** Compress audio files before transcription for better performance and faster processing.
- **File Size Limitation:** Optimized for audio files up to 25 minutes. Larger files are split into chunks automatically.

## Performance 
- **OpenAI Provider:** The latest update introduces multithreaded processing, significantly improving transcription speed. An audio file of 1 hour and 15 minutes was transcribed in just ~89.86 seconds with threading, compared to ~372.7 seconds without it. This makes the API option ideal for faster, large-scale transcription workloads.
- **Local Provider:** Running Whisper models locally can still be resource-intensive, particularly for larger model sizes.
On lower-spec or older machines, you may experience higher CPU usage and slower processing speeds.
For the best performance on such systems, the OpenAI provider remains the recommended choice.
  
## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributors

- @Marco-26 - Marco Costa

Feel free to contribute by submitting bug reports, feature requests, or pull requests!
