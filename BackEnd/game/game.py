from itertools import count
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
        self.budget_handler = BudgetHandler(self.budget, 20_000)
        self.mood = 100

        self.rounds = RoundsList()
        self.current_round = None

        self.state = "idle"

        self.mood_decay = MoodDecay(self)
        self._last_printed_sliders = None

    def start_game(self):
        self._build_rounds()
        self.state = "running"
        self.current_round = self.rounds.getNext()

        self.controls.reset_all()

        self.mood_decay.start()

        print("Game started")

    def _build_rounds(self):
        self.rounds.clear()

        # Questions
        q1 = Question("test1", 10, 10)
        q2 = Question("test2", 10, -10)
        q3 = Question("test3", 10, -10)

        q4 = Question("test4", 10,  5)
        q5 = Question("test5", 10, -5)
        q6 = Question("test6", 10, -5)

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

        if self.current_round is None:
            self._start_next_round()
            return
        
        desired = self._collect_slider_input()
        if desired:
            new_sliders = self.budget_handler.reconcile(desired)
            self._broadcast_sliders(new_sliders)

            if new_sliders != self._last_printed_sliders:
                self._print_slider_budget(new_sliders)
                self._last_printed_sliders = new_sliders.copy()

        if self.controls.check_consensus():
            print("Consensus reached")
            self._end_current_round()

    def _start_next_round(self):
        self.current_round = self.rounds.getNext()

        if self.current_round is None:
            self._end_game()
            return

        self.mood_decay.start_round()
        self.controls.reset_all()

        print(
            f"\n=== Starting Round {self.current_round.id} "
            f"({self.current_round.round_type}) ==="
        )

        self._last_printed_sliders = None

        self.controls.reset_all()

        event = self.current_round.getEvent()
        if isinstance(event, QuestionList):
            for q in event:
                print(f"Question: {q.question}")

    def _end_current_round(self):
        spent = self.budget_handler.spend_round_budget()

        print(f"Budget spent this round: {spent}")
        print(f"Remaining total budget: {self.budget_handler.total_budget}")

        if self.budget_handler.is_budget_empty():
            self._end_game()
            return
        self.current_round = None
        self.budget_handler.reset_round ()
        self.controls.reset_all()

    def _end_game(self):
        self.state = "finished"
        self.controls.reset_all()

        self.mood_decay.stop()
        if self.budget_handler.is_budget_empty():
            print("\nGame over: Budget exhausted")
        print("\nGame finished")

    def _collect_slider_input(self):
        controllers = self.controls.all_controllers()
        if not controllers:
            return None

        # Use the first controller's sliders exactly as-is
        return controllers[0].get_slider_data()

    def _broadcast_sliders(self, sliders):
        for controller in self.controls.all_controllers():
            controller.sliders = sliders.copy()

    def _print_slider_budget(self, sliders):
        total = sum(sliders)
        print(
        f"Slider inzet | "
        f"S0: {sliders[0]} | "
        f"S1: {sliders[1]} | "
        f"S2: {sliders[2]} | "
        f"Ingezet deze ronde: {total} | "
        f"Resterend spelbudget: {self.budget_handler.total_budget}"
    )

