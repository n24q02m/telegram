import importlib.util
import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch

# Load the hook module
hook_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "check-credentials.py")
)
spec = importlib.util.spec_from_file_location("check_credentials", hook_path)
assert spec is not None and spec.loader is not None
check_credentials = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_credentials)


class TestCheckCredentials(unittest.TestCase):
    @patch.dict(os.environ, {"TELEGRAM_PHONE": "123456789"}, clear=True)
    def test_is_configured_phone(self):
        self.assertTrue(check_credentials._is_configured())

    @patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "token123"}, clear=True)
    def test_is_configured_bot(self):
        self.assertTrue(check_credentials._is_configured())

    @patch.dict(os.environ, {}, clear=True)
    @patch("os.path.exists")
    @patch("os.path.expanduser")
    def test_is_configured_file(self, mock_expanduser, mock_exists):
        mock_expanduser.return_value = "/home/user"
        # Mocking exists to return True only for the home config path
        mock_exists.side_effect = lambda p: p == "/home/user/.config/mcp/config.enc"
        self.assertTrue(check_credentials._is_configured())

    @patch.dict(
        os.environ, {"CLAUDE_PLUGIN_OPTION_TELEGRAM_BOT_TOKEN": "token123"}, clear=True
    )
    @patch("os.path.exists")
    def test_is_configured_plugin_option(self, mock_exists):
        # Claude Code hands the plugin's TELEGRAM_BOT_TOKEN option to hooks as
        # CLAUDE_PLUGIN_OPTION_TELEGRAM_BOT_TOKEN; only the server sees the
        # plain TELEGRAM_BOT_TOKEN name.
        mock_exists.return_value = False
        self.assertTrue(check_credentials._is_configured())

    @patch.dict(os.environ, {}, clear=True)
    def test_is_configured_saved_store(self):
        # `telegram auth` saves to hull's store at ~/.telegram/config.json;
        # hull still reads the two pre-rename directories.
        for store_dir in (".telegram", ".telegram-mcp", ".better-telegram-mcp"):
            with self.subTest(store_dir=store_dir):
                with tempfile.TemporaryDirectory() as home:
                    os.makedirs(os.path.join(home, store_dir))
                    with open(os.path.join(home, store_dir, "config.json"), "wb"):
                        pass
                    with patch("os.path.expanduser", return_value=home):
                        self.assertTrue(check_credentials._is_configured())

    @patch.dict(os.environ, {}, clear=True)
    def test_http_settings_alone_are_not_credentials(self):
        # ~/.telegram/config.toml holds HTTP server settings, not credentials.
        with tempfile.TemporaryDirectory() as home:
            os.makedirs(os.path.join(home, ".telegram"))
            with open(os.path.join(home, ".telegram", "config.toml"), "wb"):
                pass
            with patch("os.path.expanduser", return_value=home):
                self.assertFalse(check_credentials._is_configured())

    @patch.dict(os.environ, {}, clear=True)
    @patch("os.path.exists")
    def test_not_configured(self, mock_exists):
        mock_exists.return_value = False
        self.assertFalse(check_credentials._is_configured())

    @patch("sys.stdin", io.StringIO(json.dumps({"tool_name": "any_tool__setup"})))
    @patch("sys.exit", side_effect=SystemExit)
    def test_main_exempt_tool(self, mock_exit):
        with self.assertRaises(SystemExit):
            check_credentials.main()
        mock_exit.assert_called_with(0)

    @patch.dict(os.environ, {}, clear=True)
    @patch("os.path.exists")
    @patch("sys.stdin", io.StringIO(json.dumps({"tool_name": "send_message"})))
    @patch("sys.exit", side_effect=SystemExit)
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_main_blocked(self, mock_stdout, mock_exit, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(SystemExit):
            check_credentials.main()

        mock_exit.assert_called_with(2)
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output["decision"], "block")
        self.assertTrue(
            output["reason"].startswith("telegram credentials not configured")
        )
        self.assertIn("telegram auth --bot-token", output["reason"])
        self.assertIn("telegram auth --phone", output["reason"])
        self.assertNotIn("better-telegram-mcp", output["reason"])

    @patch.dict(os.environ, {"TELEGRAM_PHONE": "123456789"}, clear=True)
    @patch("sys.stdin", io.StringIO(json.dumps({"tool_name": "send_message"})))
    @patch("sys.exit", side_effect=SystemExit)
    def test_main_allowed(self, mock_exit):
        with self.assertRaises(SystemExit):
            check_credentials.main()
        mock_exit.assert_called_with(0)

    @patch("sys.stdin", io.StringIO("invalid json"))
    @patch("sys.exit", side_effect=SystemExit(2))
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_main_invalid_json(self, mock_stdout, mock_exit):
        with self.assertRaises(SystemExit) as cm:
            check_credentials.main()

        self.assertEqual(cm.exception.code, 2)
        mock_exit.assert_called_with(2)
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output["decision"], "block")
        self.assertIn(
            "Invalid input: payload must be a JSON dictionary", output["reason"]
        )

    @patch.dict(os.environ, {}, clear=True)
    @patch("os.path.exists")
    @patch("sys.stdin", io.StringIO(json.dumps({"tool_name": 123})))
    @patch("sys.exit", side_effect=SystemExit)
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_main_invalid_tool_name_type(self, mock_stdout, mock_exit, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(SystemExit):
            check_credentials.main()

        mock_exit.assert_called_with(2)
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output["decision"], "block")
        self.assertTrue(
            output["reason"].startswith("telegram credentials not configured")
        )

    @patch("sys.stdin", io.StringIO('["not a dict"]'))
    @patch("sys.exit", side_effect=SystemExit(2))
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_main_not_dict_json(self, mock_stdout, mock_exit):
        with self.assertRaises(SystemExit) as cm:
            check_credentials.main()

        self.assertEqual(cm.exception.code, 2)
        mock_exit.assert_called_with(2)
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output["decision"], "block")
        self.assertIn(
            "Invalid input: payload must be a JSON dictionary", output["reason"]
        )


if __name__ == "__main__":
    unittest.main()

# Reflection:
# The check-credentials.py hook for the telegram plugin blocks tool access
# when no credentials (env vars or saved credential files) are found, except for
# specific tools ending in __setup, __help, or __config.
# This test suite ensures that both blocking and allow-listing logic
# work as expected, and that the hook handles malformed input gracefully.
