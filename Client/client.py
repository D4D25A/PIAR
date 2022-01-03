from tkinter import Tk, Entry
from tkinter.constants import WORD
from tkinter.scrolledtext import ScrolledText
import networking_handler
import sys

class RootWindow(Tk):
    WELCOME_TEXT = """Thanks for choosing PIAR for your privacy needs :) \nThe project is fully open source and always looking for new developers! \nBefore you join a room it is recommened to use a VPN or a proxy to hide your IP. \nWe can't control if a server owner modifies a script to log connections.\nType /help for help"""
    def __init__(self, w:int, h:int):
        super().__init__()
        self.w = w
        self.h = h
        self.inside_room = False
        self.room_handler = None
        self.username = None
        self.room_handler = None

        self.__setup_tk_config()
        self.display_widgets()
        self.render_new_msg(self.WELCOME_TEXT, 'green')

    def __setup_tk_config(self):
        self.title("PIAR - Privacy Is A Right [DEV PHASE]")
        self.resizable(width=False, height=False)
        self.geometry(f"{self.w}x{self.h}")

    def display_widgets(self):
        self.user_input = Entry(self)
        self.text_area = ScrolledText(self, bg="black", wrap=WORD)

        self.user_input.pack(side='bottom', fill='x', anchor='s')
        self.user_input.bind("<Return>", self.on_enter_pressed)

        self.text_area.pack(expand=1, fill="both")
        self.text_area.config(state='disabled') 
        self.text_area.tag_configure('red', foreground='red')
        self.text_area.tag_configure('green', foreground='green')
        self.text_area.tag_configure('purple', foreground='purple')

    def render_new_msg(self, msg, tag=None):
        if not msg.endswith("\n"):
            msg += "\n"

        self.text_area.config(state='normal')
        self.text_area.insert('end', msg, tag)
        self.text_area.config(state='disabled')
    
    def connect_to_room(self, ip , port, username):
        self.room_handler = networking_handler.RoomBackgroundHandler(self, ip, port, username) 
        if not self.room_handler.connect_to_room():
            self.render_new_msg('Failed to conenct to server...', 'red')
            return
        self.render_new_msg(f"Connected to room {ip}:{port}")

        self.room_handler.start_listening_for_data()
        self.render_new_msg("Listening for data from server", 'green')
        
        self.room_handler.verify_unique_username()

        # wait for reponse from server
        i = 0
        while self.room_handler.username_unique == "nothing":
            continue

        if not self.room_handler.username_unique:
            print("Sending username acknowledgement")
            networking_handler.Commands.acknowledge_invaild_userame(self.room_handler)
            self.render_new_msg("There is already someone inside the room with that username", "red")
            return

        self.render_new_msg("Unique username vaild inside room", 'green')
        self.room_handler.send_creds()
        self.inside_room = True

    def process_command(self, msg:str):
        cmd = msg[1::].lower().split()
        if cmd[0] == "join":
            try:
                ip = str(cmd[1])
                port = int(cmd[2])
                self.username = cmd[3]
                
                # if the ip doesn't follow the format of an
                # ipv4 address
                # if invaild_chars in ip:
                #     self.render_new_msg('Invaild ipv4 address', 'red')
                #     raise Exception()
            except:
                self.render_new_msg('join command failed! follow the format /join <IP> <PORT> <USERNAME>', 'red')
                return

            self.connect_to_room(ip, port, self.username)

        elif cmd[0] == "disconnect":
            if self.inside_room:
                self.room_handler.on_disconnect()
            else:
                self.render_new_msg("Not currently inside a room", 'red')
        
        elif cmd[0] == "help":
            self.render_new_msg("/help => displays all commands", 'purple')
            self.render_new_msg("/join <IP> <PORT> <USERNAME> => joins a new room", 'purple')
            self.render_new_msg("/disconnect => disconnect from the current room (NOT WORKING)", 'purple')

        else:
            self.render_new_msg("Invaild command", 'red')

    # checks for commands and stuff
    def on_enter_pressed(self, event):
        # get input
        msg = self.user_input.get()
        self.user_input.delete(0, 'end')

        if msg.startswith("/"):
            self.process_command(msg)
            pass

        elif self.inside_room:
            # check msg
            if len(msg) == 0:
                return
            msg = f"<{self.username}> {msg}"
            
            # send input to server 
            self.room_handler.relay_msg(msg)

root = None

def on_exit():
    global root
    root.destroy()
    root.quit()
    root.room_handler.on_disconnect()
    sys.exit()

def main():
    global root 

    root = RootWindow(1200, 800)
    root.protocol("WM_DELETE_WINDOW", on_exit)
    root.mainloop()

if __name__ == '__main__':
    main()