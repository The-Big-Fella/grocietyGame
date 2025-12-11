from game.questions.question import Question
from game.questions.questionlist import QuestionList
from game.rounds.round import Round
from game.rounds.roundslist import RoundsList


def testRoundList():
    question1 = Question("test1", 10, 1000, 10)
    question2 = Question("test2", 10, 1000, -10)

    questionlist = QuestionList()

    questionlist.append(question1)
    questionlist.append(question2)

    round1 = Round("questions")
    round2 = Round("storm")

    round1.addEvent(questionlist)
    round2.addEvent(questionlist)

    rounds = RoundsList()
    rounds.append(round1)
    rounds.append(round2)

    round = rounds.getNext()
    assert round.round_type == "questions"
    questions = round.getEvent()
    assert questions.getNext().question == "test1"
    assert questions.getNext().question == "test2"
    round = rounds.getNext()
    assert round.round_type == "storm"
