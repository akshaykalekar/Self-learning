import subprocess
import time
import requests
import signal
import os

APP_URL = "http://localhost:8080/data"
HEALTH_URL = "http://localhost:9090"


def start_app():
    process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(2)  # give servers time to start
    return process


def stop_app(process):
    process.send_signal(signal.SIGTERM)
    process.wait(timeout=5)


def test_main_endpoint():
    process = start_app()
    try:
        response = requests.get(APP_URL, timeout=2)
        assert response.status_code == 200
        assert response.json()["message"] == "Hello from main service"
    finally:
        stop_app(process)


def test_health_endpoint():
    process = start_app()
    try:
        response = requests.get(HEALTH_URL, timeout=2)
        assert response.status_code == 200
    finally:
        stop_app(process)
