class Button:
    def __init__(self, id):
        self.id = id
        self.pressed = False

    def set(self, value):
        self.pressed = bool(int(value))

    def __repr__(self):
        return f"Button{self.id}={self.pressed}"
