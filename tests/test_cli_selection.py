from contextlib import AbstractContextManager
from io import StringIO
import sys
import unittest
from unittest.mock import MagicMock, patch

from persistent_agent.config.settings import Settings
from persistent_agent.interfaces import cli


class ModelSelectionTests(unittest.TestCase):
    def test_local_selection_owns_server_and_skips_remote_config(self):
        service = MagicMock(spec=AbstractContextManager)
        model = MagicMock()
        settings = Settings(api_key="test-local-key", base_url="http://127.0.0.1:18080/v1", model="qwen3-0.6b")
        with patch.object(sys, "argv", ["cli"]), \
                patch("builtins.input", side_effect=["2", "/exit"]), \
                patch("sys.stdout", new_callable=StringIO) as output, \
                patch.object(cli, "local_settings", return_value=settings), \
                patch.object(cli, "load_settings") as remote_settings, \
                patch.object(cli, "LocalModelServer", return_value=service), \
                patch.object(cli, "OpenAICompatibleModel", return_value=model):
            cli.main()
        remote_settings.assert_not_called()
        service.__enter__.assert_called_once()
        service.__exit__.assert_called_once()
        model.close.assert_called_once()
        self.assertIn("当前模型：local", output.getvalue())

    def test_remote_selection_does_not_start_local_server(self):
        model = MagicMock()
        settings = Settings(api_key="remote-test-key", base_url="https://example.test", model="test-chat")
        with patch.object(sys, "argv", ["cli"]), \
                patch("builtins.input", side_effect=["1", "/exit"]), \
                patch("sys.stdout", new_callable=StringIO) as output, \
                patch.object(cli, "local_settings") as local_settings, \
                patch.object(cli, "load_settings", return_value=settings), \
                patch.object(cli, "LocalModelServer") as service, \
                patch.object(cli, "OpenAICompatibleModel", return_value=model):
            cli.main()
        local_settings.assert_not_called()
        service.assert_not_called()
        model.close.assert_called_once()
        self.assertIn("当前模型：deepseek", output.getvalue())

    def test_local_start_failure_does_not_create_model(self):
        settings = Settings(api_key="test-local-key", base_url="http://127.0.0.1:18080/v1", model="qwen3-0.6b")
        with patch.object(sys, "argv", ["cli", "--model", "local"]), \
                patch("sys.stdout", new_callable=StringIO) as output, \
                patch.object(cli, "local_settings", return_value=settings), \
                patch.object(cli, "LocalModelServer") as service, \
                patch.object(cli, "OpenAICompatibleModel") as model:
            service.return_value.__enter__.side_effect = RuntimeError("端口已占用")
            cli.main()
        model.assert_not_called()
        self.assertIn("端口已占用", output.getvalue())


if __name__ == "__main__":
    unittest.main()
