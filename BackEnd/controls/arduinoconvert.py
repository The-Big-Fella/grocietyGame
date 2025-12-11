from controls.controlpanel import ControlPanel


class MockArduinoConverter:
    """
    A mock that simulates 4 control panels with:
      - multiple sliders per panel
      - a button per panel
    It stores all incoming updates so tests can read them.
    """

    def __init__(self):
        self.updates = []

        configs = {
            1: ([1, 2], 3),
            2: ([4, 5], 6),
            3: ([7, 8], 9),
            4: ([10, 11], 12),
        }

        self.panels = {}

        for panel_id, (slider_ids, button_id) in configs.items():
            panel = ControlPanel(panel_id, slider_ids, button_id)

            # All updates from the panel propagate to this mock
            panel.SubscribeSliders(self._on_update)
            panel.SubscribeButton(self._on_update)

            self.panels[panel_id] = panel

    def _on_update(self, event):
        """Receive updates from sliders/buttons."""
        self.updates.append(event)

    def last_update(self):
        return self.updates[-1] if self.updates else None

    def set_slider(self, panel_id, slider_id, position):
        """Simulate slider movement."""
        panel = self.panels[panel_id]

        for slider in panel.getSliders():
            if slider.id == slider_id:
                slider.sliderposition(position)
                return

        raise ValueError(f"Slider {slider_id} not found in panel {panel_id}")

    def press_button(self, panel_id, is_pressed: bool):
        """Simulate button press."""
        panel = self.panels[panel_id]
        panel.button.is_pressed(is_pressed)


class ArduinoConverter:
    def __init__(self):
        ...
