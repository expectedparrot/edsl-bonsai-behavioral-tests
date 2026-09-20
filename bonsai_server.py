"""Manage the local Bonsai server lifecycle without a separate terminal."""

from contextlib import contextmanager
import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen



BASE_URL = "http://127.0.0.1:8087"


def server_ready():
    try:
        with urlopen(f"{BASE_URL}/health", timeout=2) as response:
            return json.load(response).get("status") == "ok"
    except (URLError, OSError, ValueError):
        return False


@contextmanager
def bonsai_server(startup_timeout=180):
    """Reuse an existing server, or own a server for the duration of the block."""
    if server_ready():
        yield
        return

    directory = Path(__file__).resolve().parent
    log_path = directory / "managed-server.log"
    print("Starting Bonsai; waiting for the model to load...", file=sys.stderr)
    with log_path.open("w") as log:
        process = subprocess.Popen(
            ["bash", str(directory / "start-server.sh")],
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        try:
            deadline = time.monotonic() + startup_timeout
            while True:
                if process.poll() is not None:
                    raise RuntimeError(
                        f"Bonsai exited with code {process.returncode}. See {log_path}"
                    )
                if server_ready():
                    break
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"Bonsai did not become ready. See {log_path}")
                time.sleep(0.25)
            yield
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
