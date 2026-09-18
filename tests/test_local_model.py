from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import zipfile

from persistent_agent.cognition.context_builder import ContextBuilder
from persistent_agent.model.base import ModelError
from persistent_agent.model import local_model
from persistent_agent.model.openai_compatible import OpenAICompatibleModel
from persistent_agent.runtime.agent_runtime import AgentRuntime
from persistent_agent.session.working_memory import WorkingMemory


class LocalDeploymentTests(unittest.TestCase):
    def test_local_config_overrides_only_child_environment(self):
        original = {"LLM_API_KEY": "remote-test-key", "LLM_BASE_URL": "https://example.test/v1"}
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, original):
            key = Path(folder) / "key.txt"
            key.write_text("test-local-key", encoding="utf-8")
            with patch.object(local_model, "KEY_FILE", key):
                settings = local_model.local_settings()
            self.assertEqual(settings.base_url, "http://127.0.0.1:18080/v1")
            self.assertEqual(settings.api_key, "test-local-key")
            self.assertEqual(os.environ["LLM_API_KEY"], "remote-test-key")
            self.assertEqual(os.environ["LLM_BASE_URL"], original["LLM_BASE_URL"])

    def test_bad_existing_download_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "models").mkdir()
            model = root / "models" / "test.gguf"
            model.write_bytes(b"existing")
            with patch.object(local_model, "DEPLOY", root), patch("urllib.request.urlopen") as fetch:
                with self.assertRaisesRegex(ValueError, "wrong SHA256"):
                    local_model.download("test.gguf", "https://example.test/model", "0" * 64)
                fetch.assert_not_called()
            self.assertEqual(model.read_bytes(), b"existing")

    def test_archive_cannot_escape_runtime(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive = root / "test.zip"
            with zipfile.ZipFile(archive, "w") as bundle:
                bundle.writestr("../outside.txt", "unexpected")
            with patch.object(local_model, "RUNTIME", root / "runtime"):
                with self.assertRaisesRegex(ValueError, "Unsafe archive"):
                    local_model.extract(archive)
            self.assertFalse((root / "outside.txt").exists())

    def test_server_is_loopback_and_bounded(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "llama-server.exe").touch()
            model = root / "model.gguf"
            model.touch()
            with patch.object(local_model, "RUNTIME", root), patch.object(local_model, "MODEL", model), \
                    patch.object(local_model, "KEY_FILE", model):
                command = local_model.server_command()
            for flag, value in (("--host", "127.0.0.1"), ("--ctx-size", "4096"),
                                ("--parallel", "1"), ("--n-predict", "512")):
                self.assertEqual(command[command.index(flag) + 1], value)


class LocalFailureTests(unittest.TestCase):
    def test_server_failure_and_truncation_do_not_save_history(self):
        cases = (
            (400, {"error": {"message": "context too long"}}),
            (200, {"id": "local", "object": "chat.completion", "created": 0,
                "model": "qwen3-0.6b", "choices": [{"index": 0, "finish_reason": "length",
                    "message": {"role": "assistant", "content": "partial"}}]}),
        )
        for status, payload in cases:
            class Handler(BaseHTTPRequestHandler):
                def do_POST(self):
                    self.rfile.read(int(self.headers["Content-Length"]))
                    body = json.dumps(payload).encode()
                    self.send_response(status)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)

                def log_message(self, *args):
                    pass

            with self.subTest(status=status), HTTPServer(("127.0.0.1", 0), Handler) as server:
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                model = OpenAICompatibleModel("local-not-a-secret",
                    f"http://127.0.0.1:{server.server_port}/v1", "qwen3-0.6b")
                memory = WorkingMemory()
                runtime = AgentRuntime(model, memory, ContextBuilder("test"))
                try:
                    with self.assertRaises(ModelError):
                        runtime.handle_message("test")
                    self.assertEqual(memory.snapshot(), [])
                finally:
                    model.close()
                    server.shutdown()
                    thread.join()


if __name__ == "__main__":
    unittest.main()
