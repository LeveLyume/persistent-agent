"""Portable Windows deployment of Qwen3; uses only Python's standard library."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import urllib.request
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DEPLOY = ROOT / "data" / "local-model"
RUNTIME = DEPLOY / "llama-b10964-cuda-13.3"
MODEL_NAME = "Qwen3-0.6B-Q8_0.gguf"
MODEL = DEPLOY / "models" / MODEL_NAME
ALIAS = "qwen3-0.6b"
PORT = 18080
KEY_FILE = DEPLOY / "api-key.txt"
RELEASE = "https://github.com/ggml-org/llama.cpp/releases/download/b10964/"
ARTIFACTS = (
    (
        "llama-b10964-bin-win-cuda-13.3-x64.zip",
        RELEASE + "llama-b10964-bin-win-cuda-13.3-x64.zip",
        "cd63ae76ad78a1540aa0f30f6c6284bab14c146d99a58f70c3f0a38cb9c62351",
    ),
    (
        "cudart-llama-bin-win-cuda-13.3-x64.zip",
        RELEASE + "cudart-llama-bin-win-cuda-13.3-x64.zip",
        "1462a050eb4c684921ba51dcc4cc488a036674c3e73e9945ee705b854808d03e",
    ),
    (
        MODEL_NAME,
        "https://huggingface.co/Qwen/Qwen3-0.6B-GGUF/resolve/"
        "23749fefcc72300e3a2ad315e1317431b06b590a/" + MODEL_NAME,
        "9465e63a22add5354d9bb4b99e90117043c7124007664907259bd16d043bb031",
    ),
)


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def download(name: str, url: str, digest: str) -> Path:
    folder = DEPLOY / ("models" if name.endswith(".gguf") else "downloads")
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / name
    if target.exists():
        if sha256(target) != digest:
            raise ValueError(f"Existing file has wrong SHA256; preserved for inspection: {target}")
        print(f"Verified existing {name}", flush=True)
        return target
    partial = target.with_suffix(target.suffix + ".part")
    print(f"Downloading {name} ...", flush=True)
    request = urllib.request.Request(url, headers={"User-Agent": "persistent-agent-local-setup"})
    with urllib.request.urlopen(request, timeout=60) as response, partial.open("wb") as output:
        shutil.copyfileobj(response, output)
    if sha256(partial) != digest:
        raise ValueError(f"Download SHA256 mismatch; not installed: {partial}")
    partial.replace(target)
    print(f"Verified {name}", flush=True)
    return target


def extract(archive: Path) -> None:
    """Reject archive paths escaping the dedicated runtime directory."""
    RUNTIME.mkdir(parents=True, exist_ok=True)
    root = RUNTIME.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            path = (root / member.filename).resolve()
            if not path.is_relative_to(root):
                raise ValueError(f"Unsafe archive path: {member.filename}")
        bundle.extractall(root)


def setup() -> None:
    if os.name != "nt":
        raise ValueError("This deployment is for Windows x64 with NVIDIA CUDA 13.3 support.")
    DEPLOY.mkdir(parents=True, exist_ok=True)
    for artifact in ARTIFACTS:
        path = download(*artifact)
        if path.suffix == ".zip":
            extract(path)
    (DEPLOY / "manifest.json").write_text(
        json.dumps({"artifacts": [dict(zip(("name", "url", "sha256"), a)) for a in ARTIFACTS]}, indent=2),
        encoding="utf-8",
    )
    if not KEY_FILE.exists():
        with KEY_FILE.open("x", encoding="utf-8") as key:
            key.write(secrets.token_urlsafe(32) + "\n")
    print(f"Installed under {DEPLOY}. No system settings were changed.")


def server_command() -> list[str]:
    binaries = list(RUNTIME.rglob("llama-server.exe"))
    if len(binaries) != 1 or not MODEL.is_file() or not KEY_FILE.is_file():
        raise ValueError("Deployment missing or ambiguous; run setup first.")
    return [
        str(binaries[0]), "--model", str(MODEL),
        "--host", "127.0.0.1", "--port", str(PORT), "--alias", ALIAS,
        "--api-key-file", str(KEY_FILE), "--cors-origins", f"http://127.0.0.1:{PORT}",
        "--ctx-size", "4096", "--parallel", "1", "--n-gpu-layers", "99",
        "--cache-ram", "0",
        "--batch-size", "256", "--ubatch-size", "128", "--threads", "8",
        "--n-predict", "512", "--no-context-shift", "--no-ui", "--offline",
        "--jinja", "--reasoning", "off", "--verbosity", "4",
        "--temp", "0.7", "--top-p", "0.8", "--top-k", "20", "--min-p", "0",
    ]


def chat_environment() -> dict[str, str]:
    if not KEY_FILE.is_file():
        raise ValueError("Local API key missing; run setup first.")
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not key:
        raise ValueError("Local API key file is empty; restore it before starting.")
    environment = os.environ.copy()
    environment.update(
        LLM_BASE_URL=f"http://127.0.0.1:{PORT}/v1",
        LLM_MODEL=ALIAS,
        LLM_API_KEY=key,
    )
    return environment


def run_child(command: list[str], environment: dict[str, str]) -> int:
    child = subprocess.Popen(command, cwd=ROOT, env=environment)
    try:
        return child.wait()
    except KeyboardInterrupt:
        # The foreground child also receives Ctrl+C. Give it time to release its resources.
        try:
            return child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            child.terminate()
            return child.wait(timeout=5)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "serve", "chat"))
    args = parser.parse_args()
    try:
        if args.action == "setup":
            setup()
            return 0
        if args.action == "serve":
            # Ignore inherited llama settings to make binding and resource limits reproducible.
            environment = {k: v for k, v in os.environ.items() if not k.upper().startswith("LLAMA_")}
            return run_child(server_command(), environment)
        print(f"Local chat: {ALIAS} at http://127.0.0.1:{PORT}/v1", flush=True)
        return run_child([sys.executable, "-m", "persistent_agent.interfaces.cli"], chat_environment())
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"Local model: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
