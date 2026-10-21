
import os
from functools import wraps

from flask import Flask, jsonify, request

from device import Device
from lamp import Lamp


app = Flask(__name__)

# Учебный ключ. Для реального развёртывания задавайте его
# через переменную окружения SMART_HOME_API_KEY.
API_KEY = os.environ.get("SMART_HOME_API_KEY", "dev-secret-key")

devices = {}
next_device_id = 1


def require_api_key(function):
    """Проверяет API-ключ перед обработкой запроса."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        supplied_key = request.headers.get("X-API-Key")

        if supplied_key != API_KEY:
            return jsonify({"error": "Недействительный или отсутствующий API-ключ"}), 401

        return function(*args, **kwargs)

    return wrapper


@app.route("/api/devices", methods=["POST"])
@require_api_key
def create_device():
    """Создаёт устройство из JSON-запроса."""
    global next_device_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Ожидается JSON-объект"}), 400

    name = data.get("name")
    device_type = data.get("type", "device")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Поле name обязательно и не должно быть пустым"}), 400

    name = name.strip()

    if len(name) > 100:
        return jsonify({"error": "Название не должно превышать 100 символов"}), 400

    if device_type not in ("device", "lamp"):
        return jsonify({"error": "type должен быть device или lamp"}), 400

    try:
        device = Lamp(name) if device_type == "lamp" else Device(name)
    except (TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

    device_id = next_device_id
    next_device_id += 1
    devices[device_id] = device

    return jsonify({
        "id": device_id,
        "name": device.name,
        "type": device_type,
        "status": device.status,
    }), 201


@app.route("/api/devices", methods=["GET"])
@require_api_key
def get_devices():
    """Возвращает список устройств."""
    result = []

    for device_id, device in devices.items():
        result.append({
            "id": device_id,
            "name": device.name,
            "status": device.status,
            "type": "lamp" if isinstance(device, Lamp) else "device",
        })

    return jsonify(result), 200


@app.route("/api/devices/<int:device_id>", methods=["DELETE"])
@require_api_key
def delete_device(device_id):
    """Удаляет устройство по идентификатору."""
    if device_id not in devices:
        return jsonify({"error": "Устройство не найдено"}), 404

    del devices[device_id]

    return jsonify({
        "message": "Устройство успешно удалено",
        "id": device_id,
    }), 200


if __name__ == "__main__":
    app.run(debug=False)
