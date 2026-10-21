
class AccessDeniedError(Exception):
    """Ошибка доступа к устройству."""


class DeviceAccessController:
    """Проверяет владельца устройства перед выполнением команды."""

    def __init__(self):
        self._owners = {}

    def register_device(self, device_id: int, owner_id: int) -> None:
        """Закрепляет устройство за владельцем."""
        self._owners[device_id] = owner_id

    def check_access(self, user, device_id: int) -> None:
        """Запрещает доступ без авторизации или права владения."""
        if user is None:
            raise AccessDeniedError("Требуется авторизация")

        owner_id = self._owners.get(device_id)

        if owner_id is None or owner_id != user.id:
            raise AccessDeniedError(
                "Нет доступа к этому устройству"
            )

    def turn_on(self, user, device_id: int, device) -> None:
        """Включает устройство после проверки доступа."""
        self.check_access(user, device_id)
        device.turn_on()

    def turn_off(self, user, device_id: int, device) -> None:
        """Выключает устройство после проверки доступа."""
        self.check_access(user, device_id)
        device.turn_off()
