import os
from typing import Optional

from app.core.config import settings


def save_uploaded_file(file_data: bytes, filename: str) -> Optional[str]:
    try:
        if not os.path.exists(settings.UPLOAD_DIR):
            os.makedirs(settings.UPLOAD_DIR)
            print(f"Created upload directory: {settings.UPLOAD_DIR}")

        file_path = os.path.join(settings.UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(file_data)
        print(f"File saved successfully: {file_path}")
        return file_path

    except Exception as e:
        print(f"Error saving uploaded file: {e}")
        return None
