class Observer ():
    def notify(self, event):
        ...


class Observable():
    def __init__(self):
        self.observers = []

    def subscribe(self, clb):
        self.observers.append(clb)

    def notify(self, event):
        for observer in self.observers:
            if callable(observer):
                observer()
