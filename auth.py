
import hashlib
import hmac
import secrets
from dataclasses import dataclass


def hash_password(password: str) -> str:
    """Создаёт стойкий хеш пароля с уникальной солью."""
    salt = secrets.token_bytes(16)
    n = 2**14
    r = 8
    p = 1

    password_hash = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=n,
        r=r,
        p=p,
        dklen=32,
    )

    return (
        f"scrypt${n}${r}${p}"
        f"${salt.hex()}${password_hash.hex()}"
    )


def verify_password(password: str, stored_hash: str) -> bool:
    """Проверяет пароль по сохранённому хешу."""
    try:
        algorithm, n, r, p, salt_hex, hash_hex = stored_hash.split("$")

        if algorithm != "scrypt":
            return False

        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        actual_hash = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(expected_hash),
        )

        return hmac.compare_digest(actual_hash, expected_hash)

    except (ValueError, TypeError, MemoryError):
        return False


@dataclass
class User:
    """Пользователь системы умного дома."""

    id: int
    username: str
    password_hash: str


class AuthManager:
    """Регистрация пользователей и проверка учётных данных."""

    def __init__(self):
        self._users = {}
        self._next_id = 1

    def register(self, username: str, password: str) -> User:
        """Регистрирует пользователя, сохраняя хеш пароля."""
        username = username.strip()

        if not username:
            raise ValueError("Логин не может быть пустым")

        if username in self._users:
            raise ValueError("Пользователь уже существует")

        if len(password) < 8:
            raise ValueError(
                "Пароль должен содержать минимум 8 символов"
            )

        user = User(
            id=self._next_id,
            username=username,
            password_hash=hash_password(password),
        )

        self._users[username] = user
        self._next_id += 1

        return user

    def login(self, username: str, password: str):
        """Возвращает пользователя только при верном пароле."""
        user = self._users.get(username.strip())

        if user is None:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user
