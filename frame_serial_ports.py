# ver = 2022-4-2-1

import serial
import serial.tools.list_ports
from tkinter import *
from constants import *
from session import Session
from user_entry import UserEntry
import sys
import tkinter.messagebox


# Class to create GUI
class FrameSerialPorts:
    # Dependencies: MainWindow communicate with classes that are related to GUI contents and buttons
    # instantiation function. Use root for GUI and refers to main window
    def __init__(self, root_frame):

        self.root = root_frame
        self.session = Session()
        self.user_entry = UserEntry()

        self.serial_port_scan()

        ######################################################################
        # GUI Frames
        # self.frame = LabelFrame(self.root, width=500, height=400, padx=0, pady=5, text="", borderwidth=0)
        self.frame = LabelFrame(self.root, text="", borderwidth=0)
        # self.frame.grid_propagate(False)

        # Grid can be called here or from MainWindow
        # self.frame.grid(row=0, column=0, sticky="W", padx=10, pady=0, ipadx=5, ipady=2)

        # Frames
        # self.frame_commands = LabelFrame(self.frame, width=0, height=30, padx=0, pady=0, text="", borderwidth=0)
        # self.frame_port_list = LabelFrame(self.frame, width=0, padx=0, pady=0, text="", borderwidth=0)
        self.frame_commands = LabelFrame(self.frame, text="", borderwidth=0)
        self.frame_port_list = LabelFrame(self.frame, text="", borderwidth=0)

        self.frame_commands.grid    (row=0, column=0, sticky="W", ipadx=5, ipady=2)
        self.frame_port_list.grid   (row=1, column=0, sticky="W", ipadx=5, ipady=2)

        # Radiobuttons
        self.radiobutton_show_port_detail_option_entry = IntVar(value=self.user_entry.show_port_detail_option)
        self.radiobutton_show_port_detail_option_1 = Radiobutton(self.frame_commands, text="Short Info",
                                                command=self.radiobutton_show_port_detail_option,
                                                variable=self.radiobutton_show_port_detail_option_entry,
                                                value=SHOW_PORT_DETAIL_SHORT)
        self.radiobutton_show_port_detail_option_1.configure(font=('Arial', 12))
        self.radiobutton_show_port_detail_option_2 = Radiobutton(self.frame_commands, text="Full Info",
                                                command=self.radiobutton_show_port_detail_option,
                                                variable=self.radiobutton_show_port_detail_option_entry,
                                                value=SHOW_PORT_DETAIL_FULL)
        self.radiobutton_show_port_detail_option_2.configure(font=('Arial', 12))

        # Checkboxes
        self.checkbox_show_hidden_ports_entry = IntVar(value=SHOW_HIDDEN_PORTS_NO)
        self.checkbox_show_hidden_ports = Checkbutton(self.frame_commands, text="Include Incompatible COM Ports",
                                                      variable=self.checkbox_show_hidden_ports_entry,
                                                      command=self.checkbox_update_show_hidden_ports)

        # Buttons
        self.button_scan_serial_ports = Button(self.frame_commands, text="Scan Ports", pady=10, width=12, fg="green",
                                               command=self.serial_port_scan_and_update_gui)
        self.button_scan_serial_ports.configure(font=('Arial', 14))
        self.button_exit = Button(self.frame_commands, text="Exit", fg='red', command=self.quit_program, pady=10,
                                  width=10)
        self.button_exit.configure(font=('Arial', 14))

        self.button_info = Button(self.frame_commands, text="Info", height=1, command=self.info)

        # Grids
        self.button_scan_serial_ports.grid      (row=0, column=0, sticky=W, padx=(0, 20))
        self.radiobutton_show_port_detail_option_1.grid  (row=0, column=1, sticky=W)
        self.radiobutton_show_port_detail_option_2.grid  (row=0, column=2, sticky=W)
        self.checkbox_show_hidden_ports.grid    (row=1, column=1, sticky=W)
        self.button_exit.grid                   (row=0, column=3, padx=(20, 10))
        self.button_info.grid                   (row=0, column=4, padx=(20, 10))

        # Labels
        self.label_ports = Label(self.frame_port_list, text="Ports Found: None", fg='blue')
        self.label_ports.configure(font=('Arial', 12))

        # Textbox
        self.textbox_ports = Text(self.frame_port_list, wrap=NONE, padx=10, pady=10)
        # bind key press to a function that returns "break"
        # self.textbox_ports.bind("<Key>", lambda e: "break")
        # Allow ctrl+c only
        self.textbox_ports.bind("<Key>", lambda e: self.control_event(e))

        self.textbox_ports_hscroll_bar = Scrollbar(self.frame_port_list, orient="horizontal")
        self.textbox_ports_hscroll_bar.config(command=self.textbox_ports.xview)

        self.textbox_ports_vscroll_bar = Scrollbar(self.frame_port_list, orient="vertical")
        self.textbox_ports_vscroll_bar.config(command=self.textbox_ports.yview)

        self.textbox_ports.config(yscrollcommand=self.textbox_ports_vscroll_bar.set)
        self.textbox_ports.config(xscrollcommand=self.textbox_ports_hscroll_bar.set)

        # Grids
        self.label_ports.grid                   (row=0, column=0, sticky=W)
        self.textbox_ports.grid                 (row=1, column=0, sticky=W)
        self.textbox_ports_vscroll_bar.grid     (row=1, column=1, sticky=NS)
        self.textbox_ports_hscroll_bar.grid     (row=2, column=0, sticky=EW)

        self.textbox_ports_clear()
        self.serial_port_scan_and_update_gui()

    ######################################################################
    @staticmethod
    def quit_program():
        # quit()  # quit() does not work with pyinstaller, use sys.exit()
        sys.exit()

    def serial_port_scan_and_update_gui(self):
        self.serial_port_scan()
        self.filter_ports_to_display()
        self.update_label_ports_count()
        # self.update_port_display_data_buffer()
        # self.textbox_buffer_populate_short_and_full_list(self.session.ports_obj_list_to_display)
        self.textbox_buffer_populate_short_and_full_dict(self.session.ports_dict_to_display)
        self.textbox_ports_populate()

    def serial_port_scan(self):
        self.session = Session()

        try:
            # Scan all serial ports
            serial_ports_obj_list = serial.tools.list_ports.comports()

            # Populate to_show and to_hide lists
            for serial_port_obj in serial_ports_obj_list:
                # Read port description and compare against to_hide list
                for item in HIDE_LIST:
                    if item in serial_port_obj.description:
                        self.session.serial_ports_to_hide_obj_list.append(serial_port_obj)
                        self.session.serial_ports_to_hide_dict[serial_port_obj.name] = serial_port_obj
                    else:
                        self.session.serial_ports_to_report_obj_list.append(serial_port_obj)
                        self.session.serial_ports_to_report_dict[serial_port_obj.name] = serial_port_obj

            self.session.serial_ports_all_dict = self.session.serial_ports_to_hide_dict | self.session.serial_ports_to_report_dict
            # self.session.serial_ports_all_dict = sorted(self.session.serial_ports_to_hide_dict.items() | self.session.serial_ports_to_report_dict.items())
            self.session.serial_ports_all_obj_list = self.session.serial_ports_to_hide_obj_list + self.session.serial_ports_to_report_obj_list

            self.session.ports_count_to_hide = len(self.session.serial_ports_to_hide_dict)
            self.session.ports_count_to_report = len(self.session.serial_ports_to_report_dict)
            self.session.ports_count_all = len(self.session.serial_ports_all_dict)

        # print("SG Test self.session.serial_ports_to_report_dict:\n", self.session.ports_count_to_report)
        # print(self.session.serial_ports_to_report_dict)
        # print("*******")
        # print("SG Test self.session.serial_ports_to_hide_dict:\n", self.session.ports_count_to_hide)
        # print(self.session.serial_ports_to_hide_dict)
        # print("*******")
        # print("SG Test self.session.serial_ports_all_dict:\n", self.session.ports_count_all)
        # print(self.session.serial_ports_all_dict)
        # print("****************************")
        # print("SG Test self.session.serial_ports_to_report_obj_list:\n", self.session.ports_count_to_report)
        # print(self.session.serial_ports_to_report_obj_list)
        # print("*******")
        # print("SG Test self.session.serial_ports_to_hide_obj_list:\n", self.session.ports_count_to_hide)
        # print(self.session.serial_ports_to_hide_obj_list)
        # print("*******")
        # print("SG Test self.session.serial_ports_all_obj_list:\n", self.session.ports_count_all)
        # print(self.session.serial_ports_all_obj_list)
        # print("****************************")

        # if self.session.ports_count_to_report != 0:
        #     print("SG Test first key: \n", list(self.session.serial_ports_to_report_dict)[0])
        #     print("SG Test first value: \n", list(self.session.serial_ports_to_report_dict.values())[0])
        #     print("SG Test type of first value: \n", type(list(self.session.serial_ports_to_report_dict.values())[0]))
        #     print("SG Test: ", list(self.session.serial_ports_to_report_dict.values())[0].name)
        # print("****************************")

        # print("SG test self.session.serial_ports_obj_list:")
        # for port in self.session.serial_ports_obj_list:
        #     print("**")
        #     print(port.device)
        #     print(port.name)
        #     # print(port.description)
        #     # print(port.hwid)
        #     # print(port.location)
        #     # print(port.manufacturer)
        #     # print(port.product)
        #     # print(port.interface)

        # except serial.SerialException as e:
        except Exception:
            message = "Incompatible Serial Device Connected, Please disconnect. Serial Exception: \n"
            e = message
            raise ValueError(e)

    def filter_ports_to_display(self):
        # Ports
        if self.user_entry.show_hidden_ports_option == SHOW_HIDDEN_PORTS_NO:
            self.session.ports_obj_list_to_display = self.session.serial_ports_to_report_obj_list
            self.session.ports_dict_to_display = self.session.serial_ports_to_report_dict
        elif self.user_entry.show_hidden_ports_option == SHOW_HIDDEN_PORTS_YES:
            self.session.ports_obj_list_to_display = self.session.serial_ports_all_obj_list
            self.session.ports_dict_to_display = self.session.serial_ports_all_dict

        # Ports Count
        if self.user_entry.show_hidden_ports_option == SHOW_HIDDEN_PORTS_NO:
            self.session.ports_count_to_display = self.session.ports_count_to_report
        elif self.user_entry.show_hidden_ports_option == SHOW_HIDDEN_PORTS_YES:
            self.session.ports_count_to_display = self.session.ports_count_all

    def update_label_ports_count(self):
        text = "Ports Found: " + str(self.session.ports_count_to_display)
        if self.session.ports_count_to_display == 0:
            self.label_ports.config(text=text, fg='red')
        else:
            self.label_ports.config(text=text, fg='blue')
        self.label_ports.grid(row=0, column=0, sticky=W)

    def update_port_display_data_buffer(self):
        if self.session.ports_count_to_display == 0:
            self.textbox_ports_display(SERIAL_PORT_NOT_CONNECTED_NAME)
        else:
            # self.textbox_buffer_populate_short_and_full_list(self.session.ports_obj_list_to_display)
            self.textbox_buffer_populate_short_and_full_dict(self.session.ports_dict_to_display)

    def textbox_ports_populate(self):
        # Clear existing text
        self.textbox_ports_clear()

        if self.session.ports_count_to_display == 0:
            self.textbox_ports_display(SERIAL_PORT_NOT_CONNECTED_NAME)

        else:
            if self.user_entry.show_port_detail_option == SHOW_PORT_DETAIL_SHORT:
                self.textbox_ports_display(self.session.display_text_short)
            if self.user_entry.show_port_detail_option == SHOW_PORT_DETAIL_FULL:
                self.textbox_ports_display(self.session.display_text_full)

    def textbox_ports_clear(self):
        # self.textbox_ports.configure(state="normal")
        self.textbox_ports.delete("1.0", "end")
        self.textbox_ports.insert("end", "")
        # self.textbox_ports.configure(state="disabled")

    def textbox_ports_display(self, text):
        # Textbox is for display only, it doesn"t read user inputs. It is enabled to insert text then disabled
        # self.textbox_ports.configure(state="normal")
        self.textbox_ports.insert("end", text)
        # self.textbox_ports.configure(state="disabled")

    def radiobutton_show_port_detail_option(self):
        radiobutton_show_port_detail_option_entry = self.radiobutton_show_port_detail_option_entry.get()
        self.user_entry.show_port_detail_option = radiobutton_show_port_detail_option_entry
        print("::self.user_entry.action: ", self.user_entry.show_port_detail_option)
        self.serial_port_scan_and_update_gui()

    @staticmethod
    def control_event(event):
        if 12 == event.state and event.keysym == 'c':
            return
        else:
            return "break"

    @staticmethod
    def info():
        tkinter.messagebox.showinfo(title="App Info",
                                    message="Serial Port Scanner\n"
                                            "rev: 2022-4-2-1\n"
                                            "Report bugs to: Salam Gabran <sgabran@google.com>")

    def checkbox_update_show_hidden_ports(self):
        show_hidden_ports = self.checkbox_show_hidden_ports_entry.get()
        self.user_entry.show_hidden_ports_option = show_hidden_ports
        print("::self.show_hidden_ports: ", self.user_entry.show_hidden_ports_option)
        self.serial_port_scan_and_update_gui()

    def textbox_buffer_populate_short_and_full_list(self, ports_obj_list):
        if self.session.ports_count_to_display != 0:
            # print(ports_obj_list)
            for port in ports_obj_list:
                self.session.display_text_full.append("  Device: " + str(port.device) + "\n")
                self.session.display_text_full.append("  Name: " + port.name + "\n")
                self.session.display_text_full.append("  Description: " + port.description + "\n")
                self.session.display_text_full.append("  ID: " + port.hwid + "\n")
                self.session.display_text_full.append("  Location: " + str(port.location) + "\n")
                self.session.display_text_full.append("  Manufacturer: " + port.manufacturer + "\n")
                self.session.display_text_full.append("  Product: " + str(port.product) + "\n")
                self.session.display_text_full.append("  Interface: " + str(port.interface) + "\n")
                self.session.display_text_full.append("==============\n\n")

                self.session.display_text_short.append("  Device: " + port.device + "\n")
                self.session.display_text_short.append("  Name: " + port.name + "\n")
                self.session.display_text_short.append("  Description: " + port.description + "\n")
                self.session.display_text_short.append("==============\n\n")

            separator = ""
            self.session.display_text_short = (separator.join(map(str, self.session.display_text_short)))
            self.session.display_text_full = (separator.join(map(str, self.session.display_text_full)))
            return 1

        else:
            self.session.display_text_short = []
            self.session.display_text_full = []
            return 0

    def textbox_buffer_populate_short_and_full_dict(self, ports_obj_dict):
        if self.session.ports_count_to_display != 0:
            # Access values in dictionary
            for port in list(ports_obj_dict.values()):
                self.session.display_text_full.append("  Device: " + str(port.device) + "\n")
                self.session.display_text_full.append("  Name: " + port.name + "\n")
                self.session.display_text_full.append("  Description: " + port.description + "\n")
                self.session.display_text_full.append("  ID: " + port.hwid + "\n")
                self.session.display_text_full.append("  Location: " + str(port.location) + "\n")
                self.session.display_text_full.append("  Manufacturer: " + port.manufacturer + "\n")
                self.session.display_text_full.append("  Product: " + str(port.product) + "\n")
                self.session.display_text_full.append("  Interface: " + str(port.interface) + "\n")
                self.session.display_text_full.append("==============\n\n")

                self.session.display_text_short.append("  Device: " + port.device + "\n")
                self.session.display_text_short.append("  Name: " + port.name + "\n")
                self.session.display_text_short.append("  Description: " + port.description + "\n")
                self.session.display_text_short.append("==============\n\n")

            separator = ""
            self.session.display_text_short = (separator.join(map(str, self.session.display_text_short)))
            self.session.display_text_full = (separator.join(map(str, self.session.display_text_full)))
            return 1

        else:
            self.session.display_text_short = []
            self.session.display_text_full = []
            return 0
