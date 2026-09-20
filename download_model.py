"""Download the pinned Apple Silicon runtime and model, verifying SHA-256."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import tarfile
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def download(url, destination, digest, check_only=False):
    if destination.exists() and sha256(destination) == digest:
        print(f"Verified {destination.name}", flush=True)
        return
    if check_only:
        raise RuntimeError(f"Missing or checksum mismatch: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    print(f"Downloading {destination.name} ...", flush=True)
    request = Request(url, headers={"User-Agent": "edsl-bonsai-behavioral-tests/0.1"})
    hasher = hashlib.sha256()
    with urlopen(request, timeout=120) as response, temporary.open("wb") as output:
        while chunk := response.read(8 * 1024 * 1024):
            output.write(chunk)
            hasher.update(chunk)
    if hasher.hexdigest() != digest:
        raise RuntimeError(f"Checksum mismatch for {temporary}; file not installed.")
    temporary.replace(destination)
    print(f"Verified {destination.name}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="Verify existing downloads without network access")
    parser.add_argument("--asset-dir", type=Path, default=HERE, help="Parent of models/ and runtime/ (default: repository)")
    args = parser.parse_args()
    if not args.check_only and (platform.system() != "Darwin" or platform.machine() != "arm64"):
        parser.error("This launcher targets Apple Silicon macOS; Linux/CUDA needs a different runtime.")
    manifest = json.loads((HERE / "downloads.json").read_text())
    archive = args.asset_dir / "runtime" / "llama-macos-arm64.tar.gz"
    runtime_url = (
        "https://github.com/PrismML-Eng/llama.cpp/releases/download/"
        f"{manifest['runtime_tag']}/{manifest['runtime_asset']}"
    )
    download(runtime_url, archive, manifest["runtime_digest"].removeprefix("sha256:"), args.check_only)
    model = manifest["model_file"]
    model_url = (
        f"https://huggingface.co/{manifest['model_repo']}/resolve/"
        f"{manifest['model_revision']}/{model['rfilename']}"
    )
    download(model_url, args.asset_dir / "models" / model["rfilename"], model["lfs"]["sha256"], args.check_only)
    if not args.check_only:
        with tarfile.open(archive, "r:gz") as bundle:
            bundle.extractall(archive.parent, filter="data")
        print("Ready. Run: uv run python ask_linda.py")


if __name__ == "__main__":
    main()
