from game.questions.question import Question
from game.questions.questionlist import QuestionList
from game.rounds.round import Round
from game.rounds.roundslist import RoundsList


class Game ():
    def __init__(self, controlManager):
        self.budget = 100000
        self.mood = 100
        self.rounds = RoundsList()
        self.controls = controlManager
        self.currentRound = None
        self.currentRoundId = None

    def start_game(self):
        question1 = Question("test1", 10, 1000, 10)
        question2 = Question("test2", 10, 1000, -10)

        questionlist1 = QuestionList()
        questionlist1.append(question1)
        questionlist1.append(question2)

        questionlist2 = QuestionList()
        question3 = Question("test3", 10, 1000, 5)
        question4 = Question("test4", 10, 1000, -5)
        questionlist2.append(question3)
        questionlist2.append(question4)

        round1 = Round(0, "questions")
        round2 = Round(1, "storm")

        round1.addEvent(questionlist1)
        round2.addEvent(questionlist2)

        # Create rounds list
        self.rounds.append(round1)
        self.rounds.append(round2)

    def NextRound(self):
        return self.rounds.getNext()

    def update(self):
        if self.currentRound is None or self.currentRound.id != self.currentRoundId:
            self.currentRound = self.rounds.getNext()
            if self.currentRound is None:
                print("No more rounds!")
                return
            self.currentRoundId = self.currentRound.id
            print(f"\n=== Starting Round {self.currentRoundId} ({
                  self.currentRound.round_type}) ===")

            # Display the questions if this round has a question event
            event = self.currentRound.getEvent()
            if isinstance(event, QuestionList):
                q = event.getNext()
                while q:
                    print(f"Question: {q.question} | costs: {q.budget}")
                    q = event.getNext()

        # Check for consensus
        if self.controls.check_consensus():
            print("Consensus reached! Moving to next round...")
            # Reset current round so next update picks the next round
            self.currentRound = None
            self.currentRoundId = None
