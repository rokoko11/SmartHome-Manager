
import json
import os
import unittest
from unittest.mock import patch, MagicMock

from telegram_notifier import send_telegram_message


class TestTelegramNotifier(unittest.TestCase):

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_credentials(self):
        self.assertFalse(send_telegram_message("Тест"))

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test-token",
        "TELEGRAM_CHAT_ID": "12345",
    })
    @patch("telegram_notifier.urlopen")
    def test_successful_send(self, mock_urlopen):
        response = MagicMock()
        response.read.return_value = json.dumps({
            "ok": True,
            "result": {"message_id": 1},
        }).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = response

        self.assertTrue(send_telegram_message("Тестовое сообщение"))
        mock_urlopen.assert_called_once()

    @patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test-token",
        "TELEGRAM_CHAT_ID": "12345",
    })
    @patch("telegram_notifier.urlopen", side_effect=TimeoutError)
    def test_network_error(self, mock_urlopen):
        self.assertFalse(send_telegram_message("Тест"))
        mock_urlopen.assert_called_once()


if __name__ == "__main__":
    unittest.main()
