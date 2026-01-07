from designpaterns.linkedlist import LinkedList


class RoundsList(LinkedList):
    def __init__(self):
        super().__init__()

    def clear(self):
        self.head = None
        self.tail = None
        self._size = 0
