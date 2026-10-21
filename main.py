from device import Device
from lamp import Lamp


def main() -> None:
    """Демонстрирует работу устройства умного дома."""
    lamp = Lamp("Освещение гостиной")
    lamp.turn_on()

    state = "включено" if lamp.status else "выключено"
    print(f"{lamp.name}: {state}")


if __name__ == "__main__":
    main()
