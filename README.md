# Audio Transcription Tool

This Python tool transcribes audio files using multiple providers: OpenAI Whisper API, Deepgram, or a local Whisper model. It can split large audio files into smaller chunks, transcribe each chunk, and combine the results into a single text file.

## Prerequisites

Before using this tool, make sure you have the following installed:

- [Python 3.7+](https://www.python.org/)
- [FFmpeg](https://ffmpeg.org/)
- API keys (set as environment variables):
  - `OPENAI_API_KEY` (required for OpenAI provider)
  - `DEEPGRAM_API_KEY` (required for Deepgram provider)

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
python src/main.py <audio_file_path> [--provider PROVIDER] [--model_size MODEL_SIZE] [--language LANGUAGE]
```

### Arguments

- `<audio_file_path>`: Path to the audio file you want to transcribe (required).
- `--provider`: Type of provider to use for transcription. Options:
  - `openai` (default) - OpenAI Whisper API
  - `deepgram` - Deepgram API (faster and often cheaper)
  - `local` - Runs Whisper model locally on your machine
- `--model_size`: (For local provider only) Whisper model size. Default: `tiny`. Options: `tiny`, `base`, `small`, `medium`, `large`, etc.
- `--language`: (Optional) ISO 639-1 language code (e.g., `en`, `es`, `fr`, `pt`). If not specified, language will be auto-detected. Must be exactly 2 letters.

### Examples

**Basic usage (auto-detect language):**

```bash
python src/main.py data/example_audio.mp3
python src/main.py data/example_audio.mp3 --provider openai
python src/main.py data/example_audio.mp3 --provider deepgram
python src/main.py data/example_audio.mp3 --provider local --model_size small
```

**With language specification:**

```bash
python src/main.py data/example_audio.mp3 --provider openai --language en
python src/main.py data/spanish_audio.mp3 --provider deepgram --language es
python src/main.py data/portuguese_audio.mp3 --provider local --language pt
```

The transcript will be saved to a file named `transcript.txt` in the project root folder.

## Features

- **Multiple Providers**: Support for OpenAI Whisper API, Deepgram, and local Whisper models
- **Language Support**: Optional language specification for improved accuracy, or auto-detection
- **Audio Splitting**: Large audio files are automatically split into smaller chunks for efficient transcription
- **Optimized Concurrent Processing**: Scales up to 30 concurrent API calls (or number of chunks, whichever is smaller) for maximum throughput
- **Structured Logging**: Tagged log messages for easy filtering and debugging
- **Provider Architecture**: Clean, extensible design using factory pattern and abstract base classes
- **Output**: Saves the transcript as a text file

## Supported Providers

### OpenAI Whisper API

- **Cost**: ~$0.006/minute
- **Max chunk size**: 10 minutes
- **Best for**: High accuracy, general-purpose transcription
- **Setup**: Requires `OPENAI_API_KEY` environment variable

### Deepgram

- **Cost**: ~$0.0059/minute (Nova-2 model)
- **Max chunk size**: 5 minutes
- **Best for**: Faster processing, cost-effective, production scale
- **Setup**: Requires `DEEPGRAM_API_KEY` environment variable

### Local Whisper

- **Cost**: Free (runs on your machine)
- **Best for**: Privacy-sensitive content, offline use
- **Setup**: No API key required, but requires local compute resources

## Recommendations

- **Audio Compression**: Compress audio files before transcription for better performance and faster processing.
- **File Size Limitation**: Optimized for audio files up to 25 minutes. Larger files are split into chunks automatically.
- **Language Specification**: If you know the language, specify it using `--language` for better accuracy and faster processing.
- **Large Files**: Files split into many chunks benefit from the improved concurrent processing - all chunks process in parallel (up to 30 concurrent workers), dramatically reducing total transcription time.

## Performance

- **Concurrent Processing**: The tool automatically scales concurrent API calls based on the number of chunks (up to 30 concurrent workers). For example, a file split into 18 chunks will process all 18 chunks concurrently, significantly reducing total transcription time.
- **OpenAI Provider**: Multithreaded processing significantly improves transcription speed. An audio file of 1 hour and 15 minutes was transcribed in just ~89.86 seconds with threading, compared to ~372.7 seconds without it. With the improved concurrent processing, files with many chunks process even faster.
- **Deepgram Provider**: Typically 5-40× faster than alternatives with sub-300ms latency. Often 2.5-3× cheaper than OpenAI. Benefits from concurrent processing for files with multiple chunks.
- **Local Provider**: Running Whisper models locally can be resource-intensive, particularly for larger model sizes. On lower-spec machines, you may experience higher CPU usage and slower processing speeds. For best performance, cloud providers are recommended.

## Language Support

The tool supports language specification for improved accuracy:

- **Auto-detection** (default): The model automatically detects the language
- **Manual specification**: Provide a 2-letter ISO 639-1 code (e.g., `en`, `es`, `fr`, `pt`)

**Why specify a language?**

- Improves accuracy by 5-15% in challenging scenarios
- Faster processing (skips detection step)
- Better handling of accented speech and technical terms
- More consistent results across similar files

## Architecture

The codebase uses a clean, extensible architecture:

- **Factory Pattern**: `TranscriberFactory` creates provider instances based on configuration
- **Abstract Base Class**: `BaseTranscriber` defines the interface all providers must implement
- **Modular Design**: Each provider is in its own file under `src/providers/`
- **Easy Extension**: Adding new providers is straightforward - just create a new class inheriting from `BaseTranscriber`
- **Structured Logging**: All log messages include tags (e.g., `[OPENAI_TRANSCRIBER]`, `[DEEPGRAM_TRANSCRIBER]`) for easy filtering and debugging
- **Optimized Concurrency**: Uses `ThreadPoolExecutor` with dynamic worker count (up to 30) based on chunk count for I/O-bound API calls

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributors

- @Marco-26 - Marco Costa

Feel free to contribute by submitting bug reports, feature requests, or pull requests!
