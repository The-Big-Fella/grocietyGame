from designpaterns.linkedlist import Node

class Question(Node):
    def __init__(self, question: str):
        super().__init__(self)
        self.question = question

    def __repr__(self):
        return self.question
