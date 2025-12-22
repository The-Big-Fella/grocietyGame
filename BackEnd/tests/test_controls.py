from game.player.player import Player
from game.questions.question import Question
from controls.arduinoconvert import MockArduinoConverter


def test_controls():
    mock = MockArduinoConverter()

    question = Question("test", 1000, 1000, 10)

    controlPanel2 = mock.panels[2]

    player2 = Player(controlPanel2)

    mock.set_slider(panel_id=2, slider_id=4, position=55)
    mock.set_slider(panel_id=2, slider_id=5, position=45)
    mock.press_button(panel_id=2, is_pressed=True)

    assert player2.Agree(question)
    assert player2.getSliderData() == {4: 55, 5: 45}
