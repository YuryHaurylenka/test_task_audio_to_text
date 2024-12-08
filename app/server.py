import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from core.config import settings
from services.asr_service import convert_mp3_to_wav, recognize_audio

if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR)
    print(f"Created upload directory: {settings.UPLOAD_DIR}")


class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code: int, response_data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())
        print(f"Response sent: {response_data}")

    def do_POST(self):
        if self.path == "/asr_path":
            print("Received POST request at /asr_path")
            try:
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)

                mp3_path = data.get("audio_path")
                if not mp3_path:
                    self._send_response(
                        400, {"error": "The 'audio_path' field is missing."}
                    )
                    return

                if not os.path.exists(mp3_path):
                    self._send_response(400, {"error": f"File not found: {mp3_path}"})
                    return

                wav_file = convert_mp3_to_wav(mp3_path)
                if not wav_file:
                    self._send_response(400, {"error": "Failed to convert MP3 to WAV."})
                    return

                result = recognize_audio(wav_file)
                self._send_response(200, result)

            except json.JSONDecodeError:
                self._send_response(400, {"error": "Invalid JSON in request body."})
            except Exception as e:
                print(f"Error processing request: {e}")
                self._send_response(500, {"error": str(e)})

        else:
            self._send_response(404, {"error": "Endpoint not found"})


def run_server():
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on port 8080...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
