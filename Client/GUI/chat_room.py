from tkinter import Entry, Frame, LabelFrame, Label, messagebox
from tkinter.scrolledtext import ScrolledText  
from time_funcs import Time
import networking_handler

class ChatRoomUIHandler(Frame):
    def __init__(self, ip, port, username):
        super().__init__() 
        self.room_ip = ip
        self.room_port = port
        self.username = username
        self.sock_handler = networking_handler.RoomBackgroundHandler(self, ip, port, username)
        self.connection_status = self.sock_handler.connect_to_room()
        if self.connection_status == 0:
            messagebox.showerror('Error', "There was an error connecting to the server")

    def display_widgets(self):
        self.user_input = Entry(self)
        self.text_area = ScrolledText(self)

        self.user_input.pack(side='bottom', fill='x', anchor='s')
        self.text_area.pack(expand=1, fill="both")

        self.user_input.configure("<Return>", self.on_enter_pressed)

    def on_enter_pressed(self):
        # get input
        msg = self.user_input.get()
        self.user_input.delete(0, 'end')
        # check msg
        if len(msg) == 0:
            pass
        # send input to server 

    
