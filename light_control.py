class Lamp:
    def __init__(self, name):
        self.name = name
        self.status = False

    def turn_on(self):
        self.status = True
        print(f"{self.name}: свет включен")

    def turn_off(self):
        self.status = False
        print(f"{self.name}: свет выключен")


lamp = Lamp("Лампа в гостиной")
lamp.turn_on()
lamp.turn_off()