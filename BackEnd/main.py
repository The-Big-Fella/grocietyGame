from controls.translationlayer import TranslationLayer
from controls.controlpanel import ControllerManager

translationlayer = TranslationLayer("/dev/ttyV1", 9600)
manager = ControllerManager()


def main():
    import time

    print("Starting translation layer + controller manager")

    while True:
        # Read from serial and decode packet
        controller_update()

        # Small sleep to avoid busy loop (optional, depends on your game loop)
        time.sleep(0.001)


def controller_update():
    result = translationlayer.update()  # this updates internal buffer

    if result:
        controller_id, controls, packet_len = result

        # Update ControllerManager with decoded data
        manager.update_from_packet(controller_id, controls)

        # Example: print controller state
        c = manager.get_controller(controller_id)
        if c:
            print(f"Controller {c.controller_id} sliders={
                c.sliders} button={c.button}")


if __name__ == "__main__":
    main()
