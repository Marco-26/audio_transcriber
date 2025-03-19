# Audio Transcription Tool

This Python script is designed to transcribe audio files using the OpenAI API. It splits large audio files into smaller chunks, transcribes each chunk separately, and then combines the transcriptions into a single text file.

## Prerequisites

Before using this tool, make sure you have the following installed:

- Python 3.0
- `openai` Python package (`pip install openai`)
- `pydub` Python package (`pip install pydub`)
- `ffmpeg` (https://ffmpeg.org/)
- An OpenAI API key set as an environment variable named `OPENAI_API_KEY`

Alternatively, you can install all dependencies by running:

```bash
pip install -r requirements.txt
```
This command will install all the required packages listed in the requirements.txt file. Make sure to set up your OpenAI API key as mentioned above. **You still have to manually install ffmpeg.**

## Usage

```bash
python transcribe.py --audio <audio_file_path>
```
- <audio_file_path>: Path to the audio file you want to transcribe.
The transcript will be saved to a file named "transcript.txt" in the project root folder.

## Features

- Audio Splitting: Large audio files are automatically split into smaller chunks for efficient transcription.
- Transcription: Transcribes audio files using the OpenAI API, either as a single chunk or multiple chunks.
- Output: Saves the transcript as a text file.

## Recommendations

- Audio Compression: It's highly recommended to compress the audio file before using this script for better performance and faster transcription.
- File Size Limitation: This tool is optimized for audio files of up to 25 minutes in duration. Larger files will be split into multiple chunks for transcription.

## Example

``` bash
python transcribe.py --audio example_audio.mp3
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributors
- @Marco-26 - Marco Costa

Feel free to contribute by submitting bug reports, feature requests, or pull requests!


