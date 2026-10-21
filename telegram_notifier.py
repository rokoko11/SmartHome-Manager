
import json
import logging
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


def send_telegram_message(message: str) -> bool:
    """Отправляет сообщение в Telegram. Возвращает результат отправки."""
    token = os.environ.get("8838337562:AAFb4n3Gb1zv4FoFZp9WyeH_rC_iNBY388I")
    chat_id = os.environ.get("1244439065")

    if not token or not chat_id:
        logger.warning("Telegram не настроен: отсутствует токен или chat_id")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": message,
    }).encode("utf-8")

    request = Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("ok"):
            logger.info("Telegram-уведомление успешно отправлено")
            return True

        logger.error("Telegram API отклонил уведомление")
        return False

    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        logger.exception("Не удалось отправить Telegram-уведомление")
        return False
