from designpaterns.linkedlist import Node


class Round(Node):
    def __init__(self, round_type):
        super().__init__(self)
        self.round_type = round_type
