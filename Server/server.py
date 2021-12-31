"""
The server needs to listen for commands and return a response. Simple right?
The commands will be from sent in the form of new_command_to_server({'cmd':COMMAND_ID}) from 
the client and the server will send back new_command_to_client({'cmd':COMMAND_ID, 'data': RES_DATA}) 
and vice versa.
"""

from GUI import welcome_page
from client_handler import Client
from room_handler import Room
from tkinter import Tk, Frame, Scrollbar, Menu
from tkinter.ttk import Notebook

import socket

class Server:
    def __init__(self, listen_ip, listen_port):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.server_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
        self.connected_clients = []
        self.rooms = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def new_room(self, room):
        self.rooms.append(room)

class Root(Tk):
    def __init__(self, main_server):
        super().__init__()
        self.main_server = main_server
        self.welcome_page = welcome_page.Welcome()

        self.__configure_window_settings()
        self.__create_menu()
        self.__create_tab_system()
        
        self.welcome_page.text.pack(expand=1, fill='both')
        self.new_tab(self.welcome_page, 'Welcome')

    def __configure_window_settings(self):
        self.wm_title("Server Controller")
        self.geometry("800x600")

    def __create_menu(self):
        self.menubar = Menu(self)
        
        self.room_menu = Menu(self.menubar, tearoff=0)
        self.room_menu.add_command(label="Host New Room", command=self.__host_new_room)
        self.menubar.add_cascade(label="Room", menu=self.room_menu)

        self.config(menu=self.menubar)
        
    def __host_new_room(self):
        # New top level window where the owner
        # specifies the port and ip of the room
        # and weather it's public or not.
        # if it's public then it gets sent
        # to the master server.
        print("Host new room pressed")

    def __create_tab_system(self):
        self.tab_handler = Notebook(self)
        self.tab_handler.pack(expand=1, fill="both")

    def new_tab(self, frame, name):
        self.tab_handler.add(frame, text=name)

server_obj = Server("192.168.0.68", 4444)
Root(server_obj).mainloop()

