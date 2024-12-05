import os


class Settings:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    VOSK_MODEL_PATH = os.getenv(
        "VOSK_MODEL_PATH",
        os.path.join(BASE_DIR, "static", "models", "vosk-model-en-us-0.22"),
    )

    UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")

    @staticmethod
    def validate_model_path():
        if not os.path.exists(Settings.VOSK_MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found: {Settings.VOSK_MODEL_PATH}. "
                "Check the path or download the model."
            )
        print(f"VOSK model path is valid: {Settings.VOSK_MODEL_PATH}")

    @staticmethod
    def ensure_upload_dir():
        if not os.path.exists(Settings.UPLOAD_DIR):
            os.makedirs(Settings.UPLOAD_DIR)
            print(f"Created upload directory: {Settings.UPLOAD_DIR}")
        else:
            print(f"Upload directory exists: {Settings.UPLOAD_DIR}")


settings = Settings()
