
import unittest
from main import Device, Lamp


class TestSmartHome(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
