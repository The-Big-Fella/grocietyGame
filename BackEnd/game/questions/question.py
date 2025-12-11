from designpaterns.linkedlist import Node


class Question(Node):
    def __init__(self, question, time, budget, mood):
        # add question to linked list
        super().__init__(self)
        self.question = question
        self.time = time
        self.budget = budget
        self.mood = mood
