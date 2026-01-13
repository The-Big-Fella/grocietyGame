from game.budget_handler import BudgetHandler
from game.mood_handler import MoodDecay
from game.questions.question import Question
from game.questions.questionlist import QuestionList
from game.rounds.round import Round
from game.rounds.roundslist import RoundsList


class Game:
    def __init__(self, control_manager):
        self.controls = control_manager

        self.budget = 100_000
        self.budget_handler = BudgetHandler(self.budget)
        self.mood = 100

        self.rounds = RoundsList()
        self.current_round = None

        self.state = "idle"

        self.mood_decay = MoodDecay(self)

    def start_game(self):
        self._build_rounds()
        self.state = "running"
        self.current_round = self.rounds.getNext()

        self.controls.reset_all()

        self.mood_decay.start()
        self.mood_decay.start_round() #eerste round starten

        print("Game started")

    def _build_rounds(self):
        self.rounds.clear()

        # Questions
        q1 = Question("test1", 10, 1000, 10)
        q2 = Question("test2", 10, 1000, -10)
        q3 = Question("test3", 10, 1000, -10)

        q4 = Question("test4", 10, 1000, 5)
        q5 = Question("test5", 10, 1000, -5)
        q6 = Question("test6", 10, 1000, -5)

        list1 = QuestionList()
        list1.append(q1)
        list1.append(q2)
        list1.append(q3)

        list2 = QuestionList()
        
        list2.append(q4)
        list2.append(q5)
        list2.append(q6)

        r1 = Round(0, "questions")
        r2 = Round(1, "storm")

        r1.addEvent(list1)
        r2.addEvent(list2)

        self.rounds.append(r1)
        self.rounds.append(r2)

    def update(self):
        if self.state != "running":
            return

        # Start next round if needed
        if self.current_round is None:
            self._start_next_round()
            return

        # Check consensus
        if self.controls.check_consensus():
            print("Consensus reached")
            self._end_current_round()

    def _start_next_round(self):
        self.current_round = self.rounds.getNext()

        if self.current_round is None:
            self._end_game()
            return

        self.mood_decay.start_round()
        self.mood_decay.start_round()
        self.controls.reset_all()

        print(
            f"\n=== Starting Round {self.current_round.id} "
            f"({self.current_round.round_type}) ==="
        )

        self.controls.reset_all()

        event = self.current_round.getEvent()
        if isinstance(event, QuestionList):
            for q in event:
                print(f"Question: {q.question} | cost: {q.budget}")

    def _end_current_round(self):
        self.current_round = None
        self.budget_handler.reset()
        self.controls.reset_all()

    def _end_game(self):
        self.state = "finished"
        self.controls.reset_all()

        self.mood_decay.stop()

        print("\nGame finished")
