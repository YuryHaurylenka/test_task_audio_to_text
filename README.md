
# Audio Speech Recognition API

This project implements a lightweight API for converting audio (MP3) to text using the VOSK Speech Recognition library.

## Features

- Accepts MP3 audio files for processing.
- Converts audio to text and provides detailed JSON response, including:
    - Speaker roles (e.g., receiver, transmitter).
    - Recognized text.
    - Duration of speech segments.
    - Speaker's gender and raised voice indication.
    - Total duration of speech for each speaker.
- API with POST endpoint.

## Requirements

- Python 3.8 or higher.
- Dependencies listed in `requirements.txt`.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YuryHaurylenka/test_task_audio_to_text
   cd test_task_audio_to_text
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download and configure VOSK model**:
    - Download the VOSK model from [VOSK Models](https://alphacephei.com/vosk/models).
    - Extract the downloaded archive into a directory.
    - Optionally, set the `VOSK_MODEL_PATH` environment variable to the absolute path of the extracted model directory.
      For example:
      ```bash
      export VOSK_MODEL_PATH=/path/to/vosk-model
      ```
    - If `VOSK_MODEL_PATH` is not set, the application will default to:
      ```bash
      static/models/vosk-model-en-us-0.22
      ```
      relative to the project's base directory. Ensure the model is available at this location.

## Configuration

The application uses a configuration file (`config.py`) for managing paths and directories.

- **`VOSK_MODEL_PATH`**: This should point to the directory containing the VOSK model files. If not set, defaults to `static/models/vosk-model-en-us-0.22`.
- **`UPLOAD_DIR`**: Directory for saving uploaded audio files. It will be created automatically if it does not exist.

## Usage

1. **Start the server**:
   ```bash
   cd app
   python server.py
   ```
   The server runs on `http://localhost:8080` by default.

2. **Make a POST request** to the `/asr_path` endpoint with JSON payload:
   ```json
   {
       "audio_path": "/path/to/audio/file.mp3"
   }
   ```

   Example using `curl`:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"audio_path": "/path/to/audio.mp3"}' http://localhost:8080/asr_path
   ```

3. **Response**:
   A JSON response containing dialog details and durations.

   Example:
   ```json
   {
       "dialog": [
           {
               "source": "receiver",
               "text": "Hello, good day",
               "duration": 5.0,
               "raised_voice": true,
               "gender": "male"
           },
           {
               "source": "transmitter",
               "text": "Good afternoon",
               "duration": 6.0,
               "raised_voice": false,
               "gender": "female"
           }
       ],
       "result_duration": {
           "receiver": 5.0,
           "transmitter": 6.0
       }
   }
   ```

## File Structure

- **`config.py`**: Configuration for paths and directories.
- **`asr.py`**: Defines request and response schemas.
- **`asr_service.py`**: Handles MP3 to WAV conversion and audio recognition.
- **`server.py`**: Runs the HTTP server and handles requests.
- **`utils.py`**: Utility functions for file handling.

## Notes

- Ensure that the `UPLOAD_DIR` exists or will be created during runtime.
- Verify that `VOSK_MODEL_PATH` points to the correct directory containing the model files, or place the model in the default path.
- The VOSK model should be compatible with your language requirements.
