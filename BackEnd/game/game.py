import time

from BackEnd.game.rounds.round import RoundState, Round


class Game:
    def __init__(self):
        self.budget = 100000
        self.mood = 100
        self.roundcount = 1
        self.concession = False

    def startgame(self, roundcount):
        if roundcount > 0:
            return self.nextround(self.mood)
        else:
            print("Mood bij het eind: ", self.mood)
            print("Game Over")

    def nextround(self, mood):
        self.mood = mood
        print("Mood bij het begin: ", self.mood)
        self.roundcount -= 1
        return round

    def getmood(self):
        return self.mood

    def setmood(self, mood):
        self.mood = mood

    def demo_game(self):
        current_round = Round("demo", 10, self.mood)

        print("In de game class is je mood: ",self.mood)

        while current_round.state == RoundState.RUNNING:
            current_round.update()
            time.sleep(1)  # alleen hier, niet in Round

        self.mood = current_round.mood

        print("In de game class is je mood: ",self.mood)
