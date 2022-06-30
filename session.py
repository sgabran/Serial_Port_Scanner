
class Session:
    def __init__(self):
        self.serial_port = None

        self.serial_ports_to_report_dict = {}
        self.serial_ports_to_hide_dict = {}
        self.serial_ports_all_dict = {}

        self.serial_ports_to_report_obj_list = []
        self.serial_ports_to_hide_obj_list = []
        self.serial_ports_all_obj_list = []

        self.ports_count_to_hide = 0
        self.ports_count_to_report = 0
        self.ports_count_all = 0

        self.ports_obj_list_to_display = []
        self.ports_dict_to_display = {}
        self.ports_count_to_display = 0
        self.display_text_full = []
        self.display_text_short = []

