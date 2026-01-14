from designpaterns.linkedlist import Node
from game.questions.question import Question # adjust path if needed
from designpaterns.linkedlist import Node

class Round(Node):
    def __init__(self, id: int, round_type: str):
        super().__init__(self)
        self.id = id
        self.round_type = round_type
        self.event = None
        self.questions = []  # List of Question instances

    def add_question(self, question: Question):
        self.questions.append(question)

    def get_questions(self):
        return self.questions

    def addEvent(self, event):
        self.event = event

    def getEvent(self):
        return self.event
