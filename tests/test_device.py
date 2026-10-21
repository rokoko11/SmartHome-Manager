
import unittest

from main import Device, Lamp


class TestSmartHome(unittest.TestCase):
    """Проверяет работу устройств умного дома."""

    def test_device_initially_off(self):
        device = Device("Розетка")
        self.assertFalse(device.status)

    def test_turn_on(self):
        device = Device("Розетка")
        device.turn_on()
        self.assertTrue(device.status)

    def test_turn_off(self):
        device = Device("Розетка")
        device.turn_on()
        device.turn_off()
        self.assertFalse(device.status)

    def test_lamp(self):
        lamp = Lamp("Освещение")
        lamp.turn_on()
        self.assertTrue(lamp.status)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Device("")

    def test_whitespace_name(self):
        with self.assertRaises(ValueError):
            Device("   ")


if __name__ == "__main__":
    unittest.main()
