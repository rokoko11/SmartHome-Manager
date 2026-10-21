
import unittest

from main import Device

from auth import AuthManager
from access_control import (
    AccessDeniedError,
    DeviceAccessController,
)

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.auth = AuthManager()
        self.user = self.auth.register("user1", "StrongPass123")

    def test_password_is_not_stored_as_plain_text(self):
        self.assertNotEqual(
            self.user.password_hash,
            "StrongPass123",
        )

    def test_login_with_correct_password(self):
        user = self.auth.login("user1", "StrongPass123")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user.id)

    def test_login_with_wrong_password(self):
        user = self.auth.login("user1", "WrongPassword")
        self.assertIsNone(user)

    def test_short_password_is_rejected(self):
        with self.assertRaises(ValueError):
            self.auth.register("user2", "123")

    def test_duplicate_username_is_rejected(self):
        with self.assertRaises(ValueError):
            self.auth.register("user1", "AnotherPass123")


class TestDeviceAccess(unittest.TestCase):
    def setUp(self):
        self.auth = AuthManager()
        self.owner = self.auth.register("owner", "OwnerPass123")
        self.other = self.auth.register("other", "OtherPass123")

        self.device = Device("Освещение гостиной")
        self.controller = DeviceAccessController()
        self.controller.register_device(1, self.owner.id)

    def test_owner_can_turn_on_device(self):
        self.controller.turn_on(self.owner, 1, self.device)
        self.assertTrue(self.device.status)

    def test_other_user_cannot_control_device(self):
        with self.assertRaises(AccessDeniedError):
            self.controller.turn_on(self.other, 1, self.device)

        self.assertFalse(self.device.status)

    def test_unauthenticated_user_is_denied(self):
        with self.assertRaises(AccessDeniedError):
            self.controller.turn_on(None, 1, self.device)

        self.assertFalse(self.device.status)

    def test_unknown_device_is_denied(self):
        with self.assertRaises(AccessDeniedError):
            self.controller.turn_on(self.owner, 999, self.device)

        self.assertFalse(self.device.status)


if __name__ == "__main__":
    unittest.main()
