
import unittest

from app import app, devices


class TestSmartHomeAPI(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        devices.clear()
        self.headers = {"X-API-Key": "dev-secret-key"}

        import app as api_module
        api_module.next_device_id = 1

    def test_create_device(self):
        response = self.client.post(
            "/api/devices",
            json={"name": "Освещение гостиной", "type": "lamp"},
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Освещение гостиной")

    def test_get_devices(self):
        self.client.post(
            "/api/devices",
            json={"name": "Розетка"},
            headers=self.headers,
        )

        response = self.client.get(
            "/api/devices",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_delete_device(self):
        created = self.client.post(
            "/api/devices",
            json={"name": "Лампа"},
            headers=self.headers,
        )
        device_id = created.get_json()["id"]

        response = self.client.delete(
            f"/api/devices/{device_id}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(device_id, devices)

    def test_missing_api_key(self):
        response = self.client.get("/api/devices")

        self.assertEqual(response.status_code, 401)

    def test_invalid_api_key(self):
        response = self.client.get(
            "/api/devices",
            headers={"X-API-Key": "wrong-key"},
        )

        self.assertEqual(response.status_code, 401)

    def test_empty_name(self):
        response = self.client.post(
            "/api/devices",
            json={"name": "   "},
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)

    def test_device_not_found(self):
        response = self.client.delete(
            "/api/devices/999",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
