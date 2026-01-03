from designpaterns.linkedlist import Node


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
