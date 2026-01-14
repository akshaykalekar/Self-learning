import requests
import subprocess
import sys
import socket
import time

APP_URL = "http://localhost:8080/data"
HEALTH_URL = "http://localhost:9090/"

def wait_for_port(host, port, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return
        except OSError:
            time.sleep(0.2)
    raise RuntimeError(f"Port {port} not available")

def start_app():
    process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    wait_for_port("localhost", 8080)
    wait_for_port("localhost", 9090)
    return process

def test_main_endpoint():
    process = start_app()
    try:
        response = requests.get(APP_URL, timeout=2)
        assert response.status_code == 200
    finally:
        process.terminate()
        process.wait()

def test_health_endpoint():
    process = start_app()
    try:
        response = requests.get(HEALTH_URL, timeout=2)
        assert response.status_code == 200
    finally:
        process.terminate()
        process.wait()
