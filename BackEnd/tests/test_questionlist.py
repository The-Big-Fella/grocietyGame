from game.questions.question import Question
from game.questions.questionlist import QuestionList


def testQuestionsList():
    question1 = Question("test1", 10, 1000, 10)
    question2 = Question("test2", 10, 1000, -10)

    questionlist = QuestionList()

    questionlist.append(question1)
    questionlist.append(question2)

    question = questionlist.getNext()
    assert question.question == "test1"
    question = questionlist.getNext()
    assert question.question == "test2"
