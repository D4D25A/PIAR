from tkinter import Entry, Frame, LabelFrame, Text, Label
from tkinter.constants import DISABLED, NORMAL, END
import datetime

class ChatRoom(Frame):
    def __init__(self):
        super().__init__()
        self.__create_entry_widget()
        self.__create_usernames_panel()
        self.__create_text_box()

    def __new_username_pane_entry(self, username):
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        widget = Label(self.username_panel, text=f"[{time}] [{username}] ")
        widget.pack()

    # time and username
    def __create_usernames_panel(self):
        self.username_panel = LabelFrame(self, width=120, bg='yellow')
        self.username_panel.pack(side='left', fill='y', anchor='w')

    def __create_text_box(self):
        self.textbox = Text(self)
        self.textbox['state'] = DISABLED
        self.textbox.pack(expand=1, fill="both")

    def __create_entry_widget(self):
        self.entry_widget = Entry(self)
        self.entry_widget.bind('<Return>', self.__on_enter_pressed)
        self.entry_widget.pack(side='bottom', fill='x', anchor='s') 

    def __display_msg_handler(self, username, msg):
        self.__new_username_pane_entry(username)
        self.textbox['state'] = NORMAL
        self.textbox.insert(END, f"{msg}\n")
        self.textbox.see(END)
        self.textbox['state'] = DISABLED

    def __on_enter_pressed(self, msg):
        msg = self.entry_widget.get()
        self.entry_widget.delete(0, 'end')
        self.__display_msg_handler('billyb0b', msg)

    def __send_msg_to_server(self, msg):
        pass

    def __on_recv_msg(self, username, msg):
        pass