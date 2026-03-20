import socket
import subprocess
import threading
import time

import requests

SERVER_URI = "https://live-translate.gerritrive.de"
MIC_FILE = "./config/mic.txt"
FFMPEG_PATH = "./bin/ffmpeg"
MEDIAMTX_PATH = "./bin/mediamtx"
MEDIAMTX_CONFIG_PATH = "./config/mediamtx.yml"


def send_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    requests.post(f"{SERVER_URI}/server-ip", data={"ip": ip})


def handle_output(process):
    for _ in process.stdout:
        pass


def start_mediamtx():
    return subprocess.Popen(
        [MEDIAMTX_PATH, MEDIAMTX_CONFIG_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def start_ffmpeg(mic):
    return subprocess.Popen(
        [
            FFMPEG_PATH,
            "-f",
            "dshow",
            "-i",
            f"audio={mic}",
            "-acodec",
            "aac",
            "-f",
            "rtsp",
            "rtsp://localhost:8554/mic",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def main():
    try:
        send_ip()

        with open(MIC_FILE, "r", encoding="utf-8") as f:
            mic = f.read().strip()

        mediamtx = start_mediamtx()
        threading.Thread(target=handle_output, args=(mediamtx,), daemon=True).start()

        time.sleep(2)

        ffmpeg = start_ffmpeg(mic)
        threading.Thread(target=handle_output, args=(ffmpeg,), daemon=True).start()

        print(f"[{time.strftime('%H:%M')}]", "Programm läuft...")

        while True:
            if mediamtx.poll() is not None or ffmpeg.poll() is not None:
                raise RuntimeError("Process stopped")

            time.sleep(2)

    except Exception as e:
        print(
            f"[{time.strftime('%H:%M')}]",
            f"Ein Fehler ({e}) ist aufgetreten. Starte das Programm neu...",
        )
        time.sleep(5)
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"[{time.strftime('%H:%M')}]", "Programm wird beendet...")
