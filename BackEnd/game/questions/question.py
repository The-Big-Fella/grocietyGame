from designpaterns.linkedlist import Node


class Question(Node):
    def __init__(self, question, time, mood):
        super().__init__(self)
        self.question = question
        self.time = time
        self.mood = mood

    def __repr__(self):
        return self.question
