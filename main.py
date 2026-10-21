
class Device:
    def __init__(self, name):
        self.name = name
        self.status = False

    def turn_on(self):
        self.status = True

    def turn_off(self):
        self.status = False


class Lamp(Device):
    pass


if __name__ == "__main__":
    lamp = Lamp("Освещение гостиной")
    lamp.turn_on()
    print(f"{lamp.name}: {'включено' if lamp.status else 'выключено'}")
