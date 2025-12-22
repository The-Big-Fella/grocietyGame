class Slider:
    def __init__(self, id):
        self.id = id
        self.value = 0

    def set(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"Slider{self.id}={self.value}"
