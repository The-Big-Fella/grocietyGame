from contextlib import contextmanager
from enum import Enum, auto

from game.Handlers import BudgetHandler
from game.Handlers import MoodDecay
from game.rounds import Question, QuestionList, RoundsList, Round


class GameState(Enum):
    START = auto()
    RUNNING = auto()
    NEXT = auto()
    IDLE = auto()


class Game:
    def __init__(self, control_manager, app):
        self.app = app
        self.controls = control_manager

        self.total_budget = 100_000
        self.mood = 100  # GLOBAL, persistent

        self.rounds = RoundsList()
        self.current_round = None

        self.budget_handler = None
        self.mood_decay = MoodDecay(self)
        self.budget = self.current_round.round_budget if self.current_round else 1337
        self.state = GameState.START


    def get_state(self):
        return {
            "state": self.state.name.lower(),
            "mood": self.mood,
            "budget": self.budget
        }

    def update(self):
        """Main update dispatcher based on current state."""
        if self.state == GameState.START:
            self._start_state()
        elif self.state == GameState.RUNNING:
            self._running_state()
        elif self.state == GameState.NEXT:
            self._next_state()
        elif self.state == GameState.IDLE:
            pass  # Could be waiting for input or idle logic

    def start_game(self):
        """Initialize and start the game."""
        self._build_rounds()
        self.state = GameState.RUNNING
        
        self.current_round = self.rounds.getNext()
        self.budget = self.current_round.round_budget

        self.controls.reset_all()
        self.mood_decay.start()
        self.mood_decay.start_round()

        print("Game started")

    def _start_state(self):
        if self.controls.check_consensus():
            print("Consensus reached to start game")
            self.start_game()

    def _running_state(self):
        if self.current_round is None:
            self._start_next_round()
            if self.current_round is None:
                self.state = GameState.NEXT
                return

        if self.controls.check_consensus():
            self._end_current_round()
            self.state = GameState.NEXT

    def _next_state(self):
        self._start_next_round()
        if self.current_round is None:
            self._end_game()
        else:
            self.state = GameState.RUNNING

    def _build_rounds(self):
        self.rounds.clear()

        question_list = QuestionList()
        question_list.append(Question("test1"))
        question_list.append(Question("test2"))
        question_list.append(Question("test3"))

        round1 = Round(0, "questions",20000)
        round1.addEvent(question_list)

        round2 = Round(1, "storm", 20000)
        round2.addEvent(question_list)

        self.rounds.append(round1)
        self.rounds.append(round2)

    def _start_next_round(self):
        self.current_round = self.rounds.getNext()

        if self.current_round is None:
            return

        self.budget_handler = BudgetHandler(
            total_budget=self.total_budget,
            max_round_budget=self.current_round.round_budget,
        )

        self.budget_handler.reset_round()
        self.mood_decay.start_round()
        self.controls.reset_all()

        print(
            f"\n=== Starting Round {self.current_round.id} "
            f"({self.current_round.round_type}) | "
            f"Round budget: {self.current_round.round_budget} ==="
        )

    def _end_current_round(self):
        spent = self.budget_handler.spend_round_budget()
        self.total_budget -= spent

        print(
            f"Ending Round {self.current_round.id} | "
            f"Spent: {spent} | Remaining total budget: {self.total_budget}"
        )


    def _end_game(self):
        self.state = GameState.START
        self.controls.reset_all()
        self.mood_decay.stop()
        print("\nGame finished. Returning to start screen.")

    @contextmanager
    def _consensus(self):
        """
        Context manager for actions that should only happen if consensus is reached.
        Usage:
            with self._consensus():
                self._end_current_round()
        """
        try:
            yield
            if self.controls.check_consensus():
                print("Consensus reached")
                self.controls.reset_all()
        except Exception as e:
            print(f"Consensus transaction failed: {e}")
