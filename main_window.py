from tkinter import *
from frame_serial_ports import FrameSerialPorts


# Class to create GUI
class MainWindow:
    # Dependencies: MainWindow communicate with classes that are related to GUI contents and buttons
    def __init__(self):  # instantiation function. Use root for GUI and refers to main window
        # Root frame
        root = Tk()
        root.title("Serial Port Scanner")
        self.root_frame = root
        # Disable resizing the window
        root.resizable(False, False)

        self.frame_serial_ports = FrameSerialPorts(root)

        # Frames
        self.frame_info = LabelFrame(self.root_frame, text="", borderwidth=0)

        # Grids
        self.frame_serial_ports.frame.grid  (row=0, column=0, sticky="W", padx=10, pady=(5, 10), ipadx=5, ipady=2)

        self.root_frame.mainloop()
