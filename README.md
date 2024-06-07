# Audio-and-Video-to-Text-Conversion

This project is an audio and video to text conversion tool designed to allow users to upload audio or video files, convert them to WAV format, and extract text from the audio using speech recognition. The core functionalities include:

- Conversion: Convert MP3 and various video formats (MP4, AVI, MOV) to WAV format.
- Transcription: Extract the audio content as text using the Sphinx speech recognizer.
- Indexing: Index detected text for easy retrieval.

The project includes a command-line interface in `Audio_Video_Main.py` and an API interface using FastAPI in `app_FastAPI.py` and `app_PostMan.py`, enabling users to interact with the service via file uploads and receive the extracted text as responses. Logging is incorporated to track the processing steps and handle errors effectively.

FILES

- Audio_Video_Main.py: Contains the core functions for converting and transcribing media files.
- app_FastAPI.py: Provides an API interface for processing files through FastAPI.
- app_PostMan.py: To run it in the PostMan for testing purpose

USAGE

1. Command-Line Interface: Run `Audio_Video_Main.py` with the path to the input file to process and transcribe.
2. API Interface: Use FastAPI to upload files and get transcriptions via endpoints provided in `app_FastAPI.py`.

#EXAMPLE COMMAND-LINE USAGE

python Audio_Video_Main.py "path_to_your_file.mp4"

#EXAMPLE FASTAPI USAGE

Start the FastAPI server:

uvicorn app_FastAPI:app --reload

Upload files via the `/process` endpoint to get the transcribed text.

## Logging

Logs are saved in `conversion_log.txt` and `fastapi_app_log.txt` to track conversion processes and API interactions, respectively.

## Dependencies

- `pydub`
- `moviepy`
- `speech_recognition`
- `fastapi`
- `uvicorn`

Ensure you have these dependencies installed to run the project successfully !!!
