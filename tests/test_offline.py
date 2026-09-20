"""Exercise reproducibility, download integrity, and lifecycle without inference."""

import asyncio
import hashlib
import io
import json
from pathlib import Path
import shutil
from unittest.mock import Mock

import pytest

import behavioral_biases
import bonsai_server
import download_model

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "behavioral_bias_run"


def test_saved_results_reproduce_published_exports(tmp_path):
    for path in DATA.glob("*.results.ep"):
        shutil.copy2(path, tmp_path / path.name)
    rows = behavioral_biases.export(tmp_path)
    published = json.loads((DATA / "responses.json").read_text())
    assert rows == published
    assert len(rows) == len({r["response_id"] for r in rows}) == 84
    assert all(r["validated"] and r["finish_reason"] == "stop" for r in rows)
    scored = [r for r in rows if r["matches_key"] is not None]
    assert len(scored) == 44
    assert sum(r["matches_key"] for r in scored) == 41


def test_prompts_and_original_source_hashes_are_preserved():
    assert behavioral_biases.conditions() == json.loads((DATA / "conditions.json").read_text())
    protocol = json.loads((DATA / "protocol.json").read_text())
    for name, expected in protocol["source_sha256"].items():
        assert hashlib.sha256((ROOT / "original_scripts" / name).read_bytes()).hexdigest() == expected


def test_verified_asset_needs_no_network(tmp_path, monkeypatch):
    asset = tmp_path / "asset"
    asset.write_bytes(b"verified")
    request = Mock(side_effect=AssertionError("No network should be used"))
    monkeypatch.setattr(download_model, "urlopen", request)
    download_model.download("https://example.invalid/asset", asset, hashlib.sha256(b"verified").hexdigest())
    request.assert_not_called()


def test_corrupt_download_does_not_replace_existing_asset(tmp_path, monkeypatch):
    asset = tmp_path / "asset"
    asset.write_bytes(b"original")
    monkeypatch.setattr(download_model, "urlopen", lambda *a, **kw: io.BytesIO(b"corrupted"))
    with pytest.raises(RuntimeError, match="Checksum mismatch"):
        download_model.download("https://example.invalid/asset", asset, hashlib.sha256(b"expected").hexdigest())
    assert asset.read_bytes() == b"original"


def test_existing_server_is_not_owned(monkeypatch):
    monkeypatch.setattr(bonsai_server, "server_ready", lambda: True)
    launch = Mock(side_effect=AssertionError("Existing server must be reused"))
    monkeypatch.setattr(bonsai_server.subprocess, "Popen", launch)
    with bonsai_server.bonsai_server():
        pass
    launch.assert_not_called()


def test_owned_server_stops_on_inference_error(tmp_path, monkeypatch):
    monkeypatch.setattr(bonsai_server, "__file__", str(tmp_path / "bonsai_server.py"))
    monkeypatch.setattr(bonsai_server, "server_ready", Mock(side_effect=[False, True]))
    process = Mock()
    process.poll.return_value = None
    monkeypatch.setattr(bonsai_server.subprocess, "Popen", Mock(return_value=process))
    with pytest.raises(ValueError, match="inference failed"):
        with bonsai_server.bonsai_server():
            raise ValueError("inference failed")
    process.terminate.assert_called_once()
    process.wait.assert_called_once_with(timeout=10)


def test_published_directory_rejected_for_execution(monkeypatch):
    monkeypatch.setattr("sys.argv", ["behavioral_biases.py", "--build-only", "--output", str(DATA)])
    with pytest.raises(SystemExit) as error:
        behavioral_biases.main()
    assert error.value.code == 2


def test_openai_compatible_transport_dependencies():
    from edsl.inference_services.services.openai_compatible_service import OpenAICompatibleService

    client = OpenAICompatibleService.async_client(api_key="local", base_url="http://127.0.0.1:8087/v1")
    asyncio.run(client.close())
