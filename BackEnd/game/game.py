
class Game:
    def __init__(self):
        self.budget = 100000
        self.mood = 100
        self.roundcount = 4

    def startgame(self, roundcount):
        if roundcount > 0:
            return self.nextround
        else:
            print("Game Over")

    def nextround(self):
        self.roundcount -= 1
        return round

    def getmood(self):
        return self.mood

    def setmood(self, mood):
        self.mood = mood

