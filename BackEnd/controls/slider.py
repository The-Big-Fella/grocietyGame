from designpaterns.observer import Observable


class Slider(Observable):
    def __init__(self, id):
        self.id = id
        super().__init__()

    def sliderposition(self, y):
        self.notify({"slider": {
            "position": y
        }})
