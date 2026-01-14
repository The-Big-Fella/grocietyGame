from .LinkedList import Node, LinkedList


class QuestionList(LinkedList):
    def __init__(self):
        super().__init__()


class Question(Node):
    def __init__(self, question, budget, mood):
        super().__init__(self)
        self.question = question
        self.budget = budget
        self.mood = mood

    def __repr__(self):
        return self.question
