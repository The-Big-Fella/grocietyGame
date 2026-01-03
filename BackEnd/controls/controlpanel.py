class Controller:
    """Represents a controller with 3 sliders and 1 button."""

    def __init__(self, controller_id: int):
        self.controller_id = controller_id
        self.sliders = [0, 0, 0]  # sliders 0..2
        self.button = 0            # state button

    def update_from_controls(self, controls: dict):
        """Update sliders and button from decoded packet dictionary."""
        self.sliders = [controls.get(i, 0) for i in range(3)]
        self.button = controls.get(3, 0)

    def __repr__(self):
        return f"<Controller {self.controller_id} sliders={self.sliders} button={self.button}>"


class ControllerManager:
    """
    Maintains Controller instances.
    Updates them when given decoded packets from TranslationLayer.
    """

    def __init__(self):
        self.controllers: dict[int, Controller] = {}

    def update_from_packet(self, controller_id: int, controls: dict):
        """
        Call this whenever a decoded packet is available.
        Creates a Controller object if necessary.
        """
        if controller_id not in self.controllers:
            self.controllers[controller_id] = Controller(controller_id)
        self.controllers[controller_id].update_from_controls(controls)

    def get_controller(self, controller_id: int):
        return self.controllers.get(controller_id)

    def all_controllers(self):
        return list(self.controllers.values())
