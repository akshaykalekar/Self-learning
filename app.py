import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import socket

APP_PORT = 8080
HEALTH_PORT = 9090


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data":
            response = {"message": "Hello from main service"}
            self._send_response(200, response)
        else:
            self._send_response(404, {"error": "Not found"})

    def _send_response(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


def run_server(port, handler):
    server = HTTPServer(("0.0.0.0", port), handler)
    server.serve_forever()


def background_worker():
    while True:
        time.sleep(5)
        hostname = socket.gethostname()
        print(f"[worker] running on {hostname}")


if __name__ == "__main__":
    # Start background worker
    threading.Thread(target=background_worker, daemon=True).start()

    # Start health server on a different port
    threading.Thread(
        target=run_server,
        args=(HEALTH_PORT, HealthHandler),
        daemon=True,
    ).start()

    print(f"Starting main server on port {APP_PORT}")
    run_server(APP_PORT, AppHandler)
