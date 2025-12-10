from designpaterns.observer import Observable


class Button(Observable):
    def __init__(self, id):
        self.id = id
        super().__init__()

    def is_pressed(self, is_pressed):
        self.notify({"id": self.id, "is_pressed": is_pressed})
