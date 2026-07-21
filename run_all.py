#!/usr/bin/env python
"""Start agent, server, and client together and stream their output.

Cross-platform alternative to run_all.sh - runs anywhere the shared
.venv works (plain PowerShell/cmd on Windows, or bash/zsh elsewhere).

Usage: python run_all.py
"""
import os
import platform
import signal
import subprocess
import sys
import threading
import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IS_WINDOWS = platform.system() == "Windows"
VENV_PYTHON = os.path.join(
    ROOT_DIR, ".venv",
    "Scripts" if IS_WINDOWS else "bin",
    "python.exe" if IS_WINDOWS else "python",
)

SERVICES = [
    ("agent", "agent", "http://localhost:5001"),
    ("server", "server", "http://localhost:5000"),
    ("client", "client", "http://localhost:8000"),
]

processes = []
shutting_down = False


def stream_output(name, pipe):
    for line in iter(pipe.readline, ""):
        print(f"[{name}] {line}", end="", flush=True)
    pipe.close()


def start_service(name, folder):
    print(f"Starting {name}...", flush=True)
    proc = subprocess.Popen(
        [VENV_PYTHON, "wsgi.py"],
        cwd=os.path.join(ROOT_DIR, folder),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    processes.append(proc)
    threading.Thread(target=stream_output, args=(name, proc.stdout), daemon=True).start()
    return proc


def shutdown():
    global shutting_down
    if shutting_down:
        return
    shutting_down = True
    print("\nStopping services...")
    for proc in processes:
        if proc.poll() is None:
            proc.terminate()
    for proc in processes:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def handle_signal(*_args):
    shutdown()
    sys.exit(0)


def main():
    if not os.path.exists(VENV_PYTHON):
        print(f"Python venv not found at {VENV_PYTHON} -- create it first (python -m venv .venv).", file=sys.stderr)
        sys.exit(1)

    signal.signal(signal.SIGINT, handle_signal)
    if not IS_WINDOWS:
        signal.signal(signal.SIGTERM, handle_signal)

    for name, folder, _url in SERVICES:
        start_service(name, folder)
        time.sleep(2)

    print("\nAll services started:")
    for name, _folder, url in SERVICES:
        print(f"  {name:<6} -> {url}")
    print("\nPress Ctrl+C to stop all services.\n")

    try:
        while True:
            for proc in processes:
                if proc.poll() is not None:
                    print(f"\n[!] A service exited unexpectedly (code {proc.returncode}). Shutting down the rest...")
                    shutdown()
                    sys.exit(1)
            time.sleep(1)
    except KeyboardInterrupt:
        handle_signal()


if __name__ == "__main__":
    main()
