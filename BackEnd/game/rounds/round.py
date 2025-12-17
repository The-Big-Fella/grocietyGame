# from designpaterns.linkedlist import Node
from BackEnd.game import game
from BackEnd.game.timer import Timer
from BackEnd.game.game import Game
import time

from enum import Enum

class RoundState(Enum):
    RUNNING = 1
    SUCCESS = 2
    FAILED = 3

class Round(Node):
    def __init__(self, round_type,time_limit):
        super().__init__(self)
        self.round_type = round_type
        self.event = None
        self.state = RoundState.RUNNING
        self.timer = Timer()
        self.time_limit = time_limit

    def update(self):
        if self.state == RoundState.RUNNING:
            if self.timer.get_seconds() > self.time_limit:
                self.state = RoundState.FAILED

    def make_concession(self):
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
        240: -5
    }

    def concession_timer(self, seconds: int):
        timer = Timer()
        while timer.elapsed_time() < seconds:
            time.sleep(1)
            print("timer2",timer.elapsed_time())
        print("gelukt!!")


    def concessiondelay(self):
        while not self.concession:
            if self.seconds_timer in self.MOOD_EVENTS: #mood penalty & timestamps taken from dictionary MOOD_EVENTS
                self.mood += self.MOOD_EVENTS[self.seconds_timer]
                game.setmood(game.getmood(self), self.mood)
            elif self.seconds_timer > 275:
                self.mood -= 10
                self.nextround()
