from .LinkedList import Node, LinkedList


class QuestionList(LinkedList):
    def __init__(self):
        super().__init__()


class Question(Node):
    def __init__(self, question: str):
        super().__init__(self)
        self.question = question

    def __repr__(self):
        return self.question
