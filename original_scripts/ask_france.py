"""Ask Bonsai through EDSL, starting a local server when needed."""

from contextlib import contextmanager
import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

from edsl import Model, QuestionFreeText


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

from edsl import QuestionMultipleChoice

def main():

    model = Model(
        "bonsai-2-27b",
        service_name="openai_compatible",
        base_url=f"{BASE_URL}/v1",
        temperature=1.0,
        max_tokens=2048,
    )

    question = QuestionMultipleChoice(
        question_name="""capital_of_france""",
        question_text="""Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. 
        As a student, she was deeply concerned with issues of discrimination and social justice, and also participated in anti-nuclear demonstrations.
        Which is more probable?
        """, 
        question_options = [
            "Linda is a bank teller.",
            "Linda is a bank teller and is active in the feminist movement."
        ]
    )

    with bonsai_server():
        results = question.by(model).run(
            disable_remote_inference=True,
            disable_remote_cache=True,
            fresh=True,
            stop_on_exception=True,
        )

    if results.select("answer.capital_of_france").first() is None:
        raise RuntimeError("Bonsai returned no answer; inspect the server log.")
    return results


if __name__ == "__main__":
    results = main()
    print(results.select("answer.capital_of_france").first())
