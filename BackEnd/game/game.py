from itertools import count
from game.budget_handler import BudgetHandler
from game.mood_handler import MoodDecay
from game.questions.question import Question
from game.questions.questionlist import QuestionList
from game.rounds.round import Round
from game.rounds.roundslist import RoundsList



class Game:
    def __init__(self, control_manager, app):
        self.app = app
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

    def _build_rounds(self, current_event_id=2):  # Set default to 2 based on your data
        self.rounds.clear()

        # 1. Fetch all rounds from the DB
        all_rounds = self.app.db.get_rounds()

        # 2. Filter for the specific event
        # This will now work because 'event_id' is present in your dict list!
        event_rounds = [
            r for r in all_rounds if r['event_id'] == current_event_id]

        if not event_rounds:
            print(f"Warning: No rounds found for Event ID {current_event_id}")
            return

        # 3. Build the Linked List structure
        for r_data in event_rounds:
            # Create Round Node
            new_round = Round(id=r_data['id'], round_type=r_data['event'])

            # 4. Fetch questions for this round
            questions_data = self.app.db.get_questions_by_round(r_data['id'])

            q_list = QuestionList()
            for q_data in questions_data:
                new_question = Question(
                    question=q_data['text'],
                    time=10,
                    budget=q_data['budget'],
                    mood=q_data['mood']
                )
                q_list.append(new_question)

            new_round.addEvent(q_list)
            self.rounds.append(new_round)

        print(f"Successfully loaded {self.rounds.size} rounds for event: {
              event_rounds[0]['event']}")

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

        totals = [0, 0, 0]

        for c in controllers:
            sliders = c.get_slider_data()
            for i in range(3):
                totals[i] += sliders[i]

        count = len(controllers)
        return [t // count for t in totals]


    
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

