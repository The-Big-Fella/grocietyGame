from controls.mockPanel import MockPanelGUI
import tkinter as tk
from controls.uart import UartMock


def main():
    uart = UartMock()

    root = tk.Tk()
    panel1 = MockPanelGUI(root, uart, "panel1")
    panel2 = MockPanelGUI(root, uart, "panel2")
    panel3 = MockPanelGUI(root, uart, "panel3")
    panel4 = MockPanelGUI(root, uart, "panel4")

    def poll_uart():
        while not uart.tx.empty():
            msg = uart.tx.get()
            print(f"[GUI SENT] {msg}")
        root.after(50, poll_uart)

    poll_uart()
    root.mainloop()


main()
