from game.questions.question import Question
from game.questions.questionlist import QuestionList
from game.rounds.round import Round
from game.rounds.roundslist import RoundsList
from game.mood_handler import MoodDecay


class Game:
    def __init__(self, control_manager, app):
        self.app = app
        self.controls = control_manager

        self.budget = 100_000
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
        # eerste round starten
        self.mood_decay.start_round()

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
        self.controls.reset_all()

    def _end_game(self):
        self.state = "finished"
        self.controls.reset_all()

        self.mood_decay.stop()

        print("\nGame finished")
