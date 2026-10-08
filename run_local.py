"""Run the LegalEase API and Streamlit frontend in one terminal."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


def stop_processes(processes: dict[str, subprocess.Popen]) -> None:
    """Stop all child processes and wait for them to exit."""
    for process in processes.values():
        if process.poll() is None:
            process.terminate()

    for process in processes.values():
        if process.poll() is None:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def main() -> int:
    """Start both local services and keep them running until interrupted."""
    processes: dict[str, subprocess.Popen] = {}

    commands = {
        "Backend": [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        "Frontend": [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(PROJECT_ROOT / "frontend" / "app.py"),
            "--server.address",
            "127.0.0.1",
            "--server.port",
            "8501",
        ],
    }

    try:
        for name, command in commands.items():
            processes[name] = subprocess.Popen(
                command,
                cwd=PROJECT_ROOT,
            )

        print("LegalEase is starting:", flush=True)
        print("  App:     http://localhost:8501", flush=True)
        print("  API:     http://localhost:8000/docs", flush=True)
        print("Press Ctrl+C to stop both services.", flush=True)

        while True:
            for name, process in processes.items():
                return_code = process.poll()
                if return_code is not None:
                    print(
                        f"{name} stopped with exit code {return_code}.",
                        file=sys.stderr,
                        flush=True,
                    )
                    return return_code or 1
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nStopping LegalEase...", flush=True)
        return 0
    finally:
        stop_processes(processes)


if __name__ == "__main__":
    raise SystemExit(main())
