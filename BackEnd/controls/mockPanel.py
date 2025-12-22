import tkinter as tk


class MockPanelGUI:
    def __init__(self, master, uart, panel_id="panel1"):
        self.uart = uart
        self.panel_id = panel_id

        master.title(f"Mock Control Panel {panel_id}")

        # Slider 1
        self.sldr1 = tk.Scale(master, from_=0, to=1023, orient=tk.HORIZONTAL,
                              label="Slider 1", command=self.slider1_changed)
        self.sldr1.pack()

        # Slider 2
        self.sldr2 = tk.Scale(master, from_=0, to=1023, orient=tk.HORIZONTAL,
                              label="Slider 2", command=self.slider2_changed)
        self.sldr2.pack()

        # Slider 3
        self.sldr3 = tk.Scale(master, from_=0, to=1023, orient=tk.HORIZONTAL,
                              label="Slider 3", command=self.slider3_changed)
        self.sldr3.pack()

        # Button
        self.btn = tk.Button(master, text="Press Me",
                             command=self.button_pressed)
        self.btn.pack(pady=10)

    def slider1_changed(self, value):
        self.uart.write(f"{self.panel_id}:SLDR1:{int(value)}")

    def slider2_changed(self, value):
        self.uart.write(f"{self.panel_id}:SLDR2:{int(value)}")

    def slider3_changed(self, value):
        self.uart.write(f"{self.panel_id}:SLDR3:{int(value)}")

    def button_pressed(self):
        self.uart.write(f"{self.panel_id}:BTN:1")
