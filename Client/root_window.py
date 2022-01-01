from tkinter import Tk, ttk
from GUI import welcome_window, public_servers, chat_room, message_win
import networking_handler

class RootWindow(Tk):
    def __init__(self, w:int, h:int):
        super().__init__()
        self.w = w
        self.h = h
        self.__setup_tk_config()
        self.tab_controller = ttk.Notebook(self)
        self.tab_controller.pack(expand=1, fill="both")

        self.__initialize_public_rooms_tab()

    def __setup_tk_config(self):
        self.title("PIAR - Privacy Is A Right [DEV PHASE]")
        self.resizable(width=False, height=False)
        self.geometry(f"{self.w}x{self.h}")

    def __initialize_public_rooms_tab(self):
        public_rooms_frame = public_servers.PublicServersFrame(self)
        self.add_new_tab(public_rooms_frame, "Public Rooms")

    def add_new_tab(self, tab_frame, name:str):
        self.tab_controller.add(tab_frame, text=name)

    def get_tab_controller(self):
        return self.tab_controller

    def connect_to_room(self, ip, port):
        print(f"Connecting to room... {ip}:{port}")
        def null():
            pass
        
        # This section is quite messy and honestly not a good solution. Since
        # it works it will be implemented now but changed later.
        ########################################################################
        username_window = message_win.UsernameEntry(250, 100, 'Username Entry')
        self.wait_window(username_window)
        username_ok = username_window.username_ok
        username = username_window.username
        if not username_ok:
            return
        #################################################################################

        room_ui = chat_room.ChatRoomUIHandler(ip, port, username )
        if room_ui.connection_status == 1:
            self.add_new_tab(room_ui, ip)
        room_ui.send_creds()
        room_ui.render_new_msg('<billyb0b> Hello david')



root = RootWindow(1200, 800)
root.mainloop()