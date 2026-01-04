# Audio Transcriber - Copilot Instructions

## Architecture Overview

This is an audio transcription tool with two provider backends:
- **CloudTranscriber**: Uses OpenAI Whisper API with multithreaded chunk processing
- **LocalTranscriber**: Uses `faster-whisper` for on-device transcription

The `Transcriber` class in [src/transcriber.py](../src/transcriber.py) acts as a facade, delegating to the appropriate provider based on the `--provider` argument.

### Data Flow (Cloud)
1. Audio loaded via `pydub.AudioSegment`
2. If >10 minutes: split into chunks → export to `output_chunks/` → parallel API calls via `ThreadPoolExecutor` → join results → cleanup temp files
3. If ≤10 minutes: single API call

## Key Files
- [src/main.py](../src/main.py) - CLI entry point with argparse
- [src/transcriber.py](../src/transcriber.py) - Core transcription logic (both providers)
- [src/constants.py](../src/constants.py) - Configuration: `MODEL_SIZES`, `WORKER_THREAD_COUNT`, API key loading
- [src/utils.py](../src/utils.py) - File validation (`python-magic` for MIME check), transcript saving

## Development Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
brew install ffmpeg  # Required for pydub
```
Set `OPENAI_API_KEY` in `.env` file (loaded via `python-dotenv`).

## Running
```bash
python src/main.py <audio_file.mp3> --provider openai
python src/main.py <audio_file.mp3> --provider local --model_size small
```

## Project Conventions

### Threading Pattern
- `CloudTranscriber.__threading_transcription()` uses `ThreadPoolExecutor.map()` for ordered parallel transcription
- `WORKER_THREAD_COUNT` (default 4) in constants.py controls concurrency
- `pool.map()` preserves input order—no manual index tracking needed

### Error Handling
- Validation errors raise `ValueError` or `FileNotFoundError`
- Runtime errors wrapped in `RuntimeError` with logging
- All exceptions caught and logged in `main.py`

### File Validation
- Uses `python-magic` for MIME type checking (currently only `audio/mpeg` allowed)
- Path validation via `pathlib.Path`

### Temporary Files
- Chunks stored in `output_chunks/` directory
- Cleaned up via `shutil.rmtree()` after transcription completes
- **Note**: Cleanup doesn't run if transcription fails mid-process

## Known Limitations & TODOs
- No retry/backoff for API rate limits
- No per-request timeouts on OpenAI calls
- Cleanup should use `finally` block for robustness
- Only MP3 format currently supported (MIME check in utils.py)
- `LocalTranscriber` writes to `transcription.txt` but doesn't use it (dead code)

## Model Sizes
Local provider supports Whisper model sizes defined in `MODEL_SIZES` (constants.py): `tiny`, `base`, `small`, `medium`, `large-v3`, `turbo`, etc.
