from .LinkedList import Node, LinkedList


class QuestionList(LinkedList):
    def __init__(self):
        super().__init__()


class Question(Node):
    def __init__(self, question: str, spentbudget: int = 0):
        super().__init__(self)
        self.question = question
        self.spent_budget = spentbudget

    def __repr__(self):
        return self.question
