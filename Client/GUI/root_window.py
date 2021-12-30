from tkinter import Tk, ttk

class RootWindow(Tk):
    def __init__(self, w:int, h:int):
        super().__init__()
        self.w = w
        self.h = h
        self.__setup_tk_config()
        self.tab_controller = ttk.Notebook(self)
        self.tab_controller.pack(expand=1, fill="both")

    def __setup_tk_config(self):
        self.title("PIAR - Privacy Is A Right [DEV PHASE]")
        self.resizable(width=False, height=False)
        self.geometry(f"{self.w}x{self.h}")

    def add_new_tab(self, tab_frame, name:str):
        self.tab_controller.add(tab_frame, text=name)

    def get_tab_controller(self):
        return self.tab_controller
