import json
import wave
from typing import Optional

from pydub import AudioSegment
from vosk import KaldiRecognizer, Model

from app.core.config import settings

try:
    model = Model(settings.VOSK_MODEL_PATH)
    print(f"Loaded VOSK model from: {settings.VOSK_MODEL_PATH}")
except Exception as e:
    print(f"Error loading VOSK model: {e}")
    raise


def convert_mp3_to_wav(mp3_path: str) -> Optional[str]:
    try:
        audio = AudioSegment.from_mp3(mp3_path)
        print(f"MP3 details: {audio.frame_rate} Hz, {audio.channels} channels")

        audio = audio.set_frame_rate(16000).set_channels(1)
        wav_path = mp3_path.replace(".mp3", ".wav")
        audio.export(wav_path, format="wav")
        print(f"Converted MP3 to WAV: {wav_path}")
        return wav_path
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        return None


def recognize_audio(wav_path: str) -> dict:
    try:
        with wave.open(wav_path, "rb") as wf:
            print(f"Processing WAV file: {wav_path}")

            # Validate WAV file parameters
            if wf.getframerate() != 16000 or wf.getnchannels() != 1:
                print(
                    f"Invalid WAV format: {wf.getframerate()} Hz, "
                    f"{wf.getnchannels()} channels. Expected 16kHz mono."
                )
                return {
                    "dialog": [],
                    "result_duration": {"receiver": 0, "transmitter": 0},
                }

            recognizer = KaldiRecognizer(model, wf.getframerate())
            result = {"dialog": []}
            receiver_duration = 0
            transmitter_duration = 0
            current_speaker = "receiver"

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    res = json.loads(recognizer.Result())
                    print(f"Intermediate recognition result: {res}")
                    text = res.get("text", "")
                    if text:
                        duration = round(wf.tell() / wf.getframerate(), 2)
                        print(f"Recognized text: {text}, Duration: {duration}")

                        result["dialog"].append(
                            {
                                "source": current_speaker,
                                "text": text,
                                "duration": duration,
                                "raised_voice": len(text.split()) > 5,
                                "gender": (
                                    "male"
                                    if current_speaker == "receiver"
                                    else "female"
                                ),
                            }
                        )
                        if current_speaker == "receiver":
                            receiver_duration += duration
                        else:
                            transmitter_duration += duration

                        current_speaker = (
                            "transmitter"
                            if current_speaker == "receiver"
                            else "receiver"
                        )

            result["result_duration"] = {
                "receiver": receiver_duration,
                "transmitter": transmitter_duration,
            }
            print("Recognition complete.")
            return result

    except Exception as e:
        print(f"Error recognizing audio: {e}")
        return {"dialog": [], "result_duration": {"receiver": 0, "transmitter": 0}}
