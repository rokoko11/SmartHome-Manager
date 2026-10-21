
class Device:
    """Базовый класс устройства умного дома."""

    def __init__(self, name: str) -> None:
        """Создаёт устройство с указанным названием."""
        if not name.strip():
            raise ValueError("Название устройства не может быть пустым")

        self.name = name
        self.status = False

    def turn_on(self) -> None:
        """Включает устройство."""
        self.status = True

    def turn_off(self) -> None:
        """Выключает устройство."""
        self.status = False
