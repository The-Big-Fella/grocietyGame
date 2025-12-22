import time

from BackEnd.game import timer
from BackEnd.game.game import Game
from BackEnd.game.timer import Timer
from game.questions.question import Question
from game.questions.questionlist import QuestionList
from game.rounds.round import Round
from game.rounds.roundslist import RoundsList

def main():
    game = Game()
    game.demo_game()


if __name__ == "__main__":
    main()


#    game = Game()
#    game.startgame()
#
#     question1 = Question("test1", 10, 1000, 10)
#     question2 = Question("test2", 10, 1000, -10)
#
#     questionlist = QuestionList()
#
#     questionlist.append(question1)
#     questionlist.append(question2)
#
#     round1 = Round("questions")
#     round2 = Round("storm")
#
#     round1.addEvent(questionlist)
#     round2.addEvent(questionlist)
#
#     rounds = RoundsList()
#     rounds.append(round1)
#     rounds.append(round2)
#
#     round = rounds.getNext()
#     print(round.getEvent().getNext().question)
#
#
# main()
