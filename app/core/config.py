import os


class Settings:
    VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "model/vosk-model-ru-0.22")
    UPLOAD_DIR = "static/uploads"


settings = Settings()
