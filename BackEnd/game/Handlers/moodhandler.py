import time
import threading


class MoodDecay:
    def __init__(self, game, post_penalty_delay=30, post_penalty_amount=10):
        self.game = game
        self.running = False
        self.thread = None

        # Locked-in penalty schedule (seconds since round start, penalty)
        self.timeline = [
            (150, 5),
            (240, 5),
            (300, 5),
            (360, 5),
        ]

        self.start_time = None
        self.next_index = 0

        # Post-penalty configuration
        self.post_penalty_delay = post_penalty_delay
        self.post_penalty_amount = post_penalty_amount
        self.post_penalty_started = False
        self.post_penalty_start_time = None

    def get_timer_info(self):
        """
        Returns a dict with detailed timer + mood decay state.
        Safe to call at any time.
        """

        if self.start_time is None:
            return {
                "active": False,
                "message": "Round not started",
            }

        now = time.monotonic()
        elapsed = now - self.start_time

        # Timeline bounds
        min_time = self.timeline[0][0] if self.timeline else 0
        max_time = self.timeline[-1][0] if self.timeline else 0

        # Penalties applied so far
        penalties_applied = self.timeline[:self.next_index]
        mood_lost_so_far = sum(p for _, p in penalties_applied)

        # Remaining penalties
        penalties_remaining = self.timeline[self.next_index:]

        # Next scheduled penalty
        if self.next_index < len(self.timeline):
            next_time, next_penalty = self.timeline[self.next_index]
            time_to_next = max(0, next_time - elapsed)
        else:
            next_time = None
            next_penalty = None
            time_to_next = None

        # Post-penalty timing
        post_info = None
        if self.post_penalty_started:
            post_elapsed = now - self.post_penalty_start_time
            post_remaining = max(0, self.post_penalty_delay - post_elapsed)
            post_info = {
                "elapsed": round(post_elapsed, 2),
                "remaining": round(post_remaining, 2),
                "penalty_amount": self.post_penalty_amount,
            }

        return {
            "active": True,
            "elapsed_time": round(elapsed, 2),

            "timeline": {
                "min_time": min_time,
                "max_time": max_time,
                "total_events": len(self.timeline),
                "events_remaining": len(penalties_remaining),
            },

            "mood_decay": {
                "lost_so_far": mood_lost_so_far,
                "current_mood": self.game.mood,
            },

            "next_penalty": {
                "time": next_time,
                "amount": next_penalty,
                "time_remaining": None if time_to_next is None else round(time_to_next, 2),
            },

            "post_penalty": post_info,
        }

    def _run(self):
        while self.running:
            if self.start_time is None:
                time.sleep(0.1)
                continue

            elapsed = time.monotonic() - self.start_time

            # Apply all scheduled penalties
            while (
                self.next_index < len(self.timeline)
                and elapsed >= self.timeline[self.next_index][0]
            ):
                trigger_time, penalty = self.timeline[self.next_index]
                self.game.mood = max(0, self.game.mood - penalty)
                print(f"[MoodDecay] {trigger_time}s → mood {self.game.mood}")
                self.next_index += 1

            # Check if timeline is done and post-penalty timer has not started
            if self.next_index >= len(self.timeline) and not self.post_penalty_started:
                # Start post-penalty timer dynamically after last scheduled penalty
                self.post_penalty_start_time = time.monotonic()
                self.post_penalty_started = True
                print("[MoodDecay] Post-penalty timer started")

            # Handle post-penalty logic
            if self.post_penalty_started:
                post_elapsed = time.monotonic() - self.post_penalty_start_time
                if post_elapsed >= self.post_penalty_delay:
                    # Apply extra mood penalty
                    self.game.mood = max(
                        0, self.game.mood - self.post_penalty_amount)
                    print(
                        f"[MoodDecay] Post-penalty applied → mood {self.game.mood}")

                    # Automatically end the round if still active
                    if self.game.current_round is not None:
                        print("[MoodDecay] Ending round due to no consensus")
                        self.game._end_current_round()

                    # Reset for next round
                    self.post_penalty_started = False
                    self.start_time = None

            time.sleep(0.1)

    def start(self):

        print("[MoodDecay] start")
        if not self.running:
            self.running = True
            self.thread = threading.Thread(
                target=self._run,
                daemon=True
            )
            self.thread.start()

    def start_round(self):
        """Call at the start of each round"""
        self.start_time = time.monotonic()
        self.next_index = 0
        self.post_penalty_started = False
        self.post_penalty_start_time = None
        print("[MoodDecay] Round timer reset")

    def stop(self):
        self.running = False

        
