# from designpaterns.linkedlist import Node
from BackEnd.game.timer import Timer
import time

from enum import Enum

class RoundState(Enum):
    RUNNING = 1
    SUCCESS = 2
    FAILED = 3

class Round:
    def __init__(self, round_type,time_limit, mood):
        super().__init__()
        self.round_type = round_type
        self.event = None
        self.state = RoundState.RUNNING
        self.timer = Timer()
        self.time_limit = time_limit
        self.seconds = 0
        self.concession = False
        self.mood = mood
        self.applied_mood_events = set()


    def update(self):
        if self.state != RoundState.RUNNING:
            return

        elapsed = int(self.timer.elapsed_time())
        print("Round - elapsed time: ", elapsed)

        # Mood penalties
        if elapsed in self.MOOD_EVENTS and elapsed not in self.applied_mood_events:
            self.mood += self.MOOD_EVENTS[elapsed]
            self.applied_mood_events.add(elapsed)
            print("Mood penalty! Mood:", self.mood)

        # Time over
        if elapsed >= self.time_limit:
            self.state = RoundState.FAILED
            print("Ronde voorbij! je mood is nu: ", self.mood)

    def no_concession(self):
        if self.state == RoundState.RUNNING:
            if self.timer.elapsed_time() > self.time_limit:
                self.state = RoundState.FAILED

    def made_concession(self):
        if self.state == RoundState.RUNNING:
            self.state = RoundState.SUCCESS

    def getEvent(self):
        return self.event

    def addEvent(self, event):
        self.event = event

    # logica voor concessie straffen

    MOOD_EVENTS = {  #timestamp + moodstraf
        90: -5,
        150: -5,
        195: -5,
        240: -5,
        2: -5,
        4: -5,
        6: -5,
        8: -5
    }

    # def concession_timer(self, seconds: int):
    #     timer = Timer()
    #     while timer.elapsed_time() < seconds:
    #         time.sleep(1)
    #         self.seconds+=1
    #         print("Elapsed time: ",timer.elapsed_time())
    #         if self.seconds in self.MOOD_EVENTS:
    #             self.concessiondelay()
    #     return self.mood
    #
    #
    # def concessiondelay(self):
    #         if self.seconds in self.MOOD_EVENTS: #mood penalty & timestamps taken from dictionary MOOD_EVENTS
    #             self.mood += self.MOOD_EVENTS[self.seconds]
    #             print("Je hebt een moodstraf gekregen! Huidige mood:", self.mood)
    #         elif self.concession_timer > self.time_limit:
    #             self.mood -= 10
    #             self.no_concession()
    #             return
