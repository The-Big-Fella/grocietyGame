class Game:

    concession = False
    seconds_timer = 0 #TODO echte timer maken
    MOOD_EVENTS = { #TODO deze verplaatsen naar de round class? als we verschillende tijden/straffen willen
        90: -5,
        150: -5,
        195: -5,
        240: -5
    }

    def __init__(self):
        self.budget = 100000
        self.mood = 100

    def startgame(self, roundcount):
        if roundcount > 0:
            return self.nextround
        else:
            print("Game Over")

    def nextround(self, question):
        print(question)
        self.seconds_timer = 0



    def concessiondelay(self):
        while not self.concession:
            if self.seconds_timer in self.MOOD_EVENTS: #mood penalty & timestamps taken from dictionary MOOD_EVENTS
                self.mood += self.MOOD_EVENTS[self.seconds_timer]
            elif self.seconds_timer > 275:
                self.mood -= 10
                self.nextround()