
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash


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
        """Регистрирует пользователя, сохраняя только хеш пароля."""
        username = username.strip()

        if not username:
            raise ValueError("Логин не может быть пустым")

        if username in self._users:
            raise ValueError("Пользователь уже существует")

        if len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")

        user = User(
            id=self._next_id,
            username=username,
            password_hash=generate_password_hash(
                password,
                method="scrypt",
            ),
        )

        self._users[username] = user
        self._next_id += 1
        return user

    def login(self, username: str, password: str):
        """Возвращает пользователя при успешной проверке пароля."""
        user = self._users.get(username.strip())

        if user is None:
            return None

        if not check_password_hash(user.password_hash, password):
            return None

        return user
