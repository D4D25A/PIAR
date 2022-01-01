import pickle
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
        self.client_obj = networking_handler.RoomBackgroundHandler(self, ip, port, username)
        self.connection_status = self.client_obj.connect_to_room()
        if self.connection_status == 0:
            messagebox.showerror('Error', "There was an error connecting to the server")
            return

        data = pickle.dumps({'command':3, 'username':self.username})
        self.client_obj.s.send(data)
        data = self.client_obj.s.recv(1024)
        print(data)
        try:
            res = data.decode('utf-8')
        except:
            data = pickle.loads(data)
            res = data['msg']

        print(res)
        if res == "NO":
            messagebox.showerror('Error', "Try a different username")
            return

        self.display_widgets()
        self.client_obj.data_listener_tr.start()
        # self.send_creds()

    # send username, public_key
    def send_creds(self):
        networking_handler.Commands.send_creds_to_server(
            self.client_obj, 
            self.username, 
            self.client_obj.public_key
        )

    def display_widgets(self):
        self.user_input = Entry(self)
        self.text_area = ScrolledText(self)

        self.user_input.pack(side='bottom', fill='x', anchor='s')
        self.user_input.bind("<Return>", self.on_enter_pressed)

        self.text_area.pack(expand=1, fill="both")
        self.text_area.config(state='disabled')

    def render_new_msg(self, msg):
        print(msg)
        if not msg.endswith("\n"):
            msg += "\n"

        self.text_area.config(state='normal')
        self.text_area.insert('end', msg)
        self.text_area.config(state='disabled')

    def on_enter_pressed(self, event):
        # get input
        msg = self.user_input.get()
        self.user_input.delete(0, 'end')
        
        # check msg
        if len(msg) == 0:
            return
        msg = f"<{self.username}> {msg}"
        
        # send input to server 
        self.client_obj.relay_msg(msg)
        
        
    
