from .LinkedList import Node, LinkedList


class RoundsList(LinkedList):
    def __init__(self):
        super().__init__()

    def clear(self):
        self.head = None
        self.tail = None
        self._size = 0


class Round(Node):
    def __init__(self, id, round_type):
        super().__init__(self)
        self.id = id
        self.round_type = round_type
        self.event = None

    def getEvent(self):
        return self.event

    def addEvent(self, event):
        self.event = event
