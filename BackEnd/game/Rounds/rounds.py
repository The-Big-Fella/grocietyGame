from .LinkedList import Node, LinkedList


class RoundsList(LinkedList):
    def __init__(self):
        super().__init__()

    def clear(self):
        self.head = None
        self.tail = None
        self._size = 0


class Round(Node):
    def __init__(self, id, round_type, round_budget: int):
        super().__init__(self)
        self.id = id
        self.round_type = round_type
        self.round_budget = round_budget
        self.event = None

    def addEvent(self, event):
        self.event = event

    def getEvent(self):
        return self.event

