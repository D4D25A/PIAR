from tkinter import Frame, ttk
from networking_handler import get_public_rooms

class PublicServersFrame(Frame):
    def __init__(self):
        super().__init__(background='red')
        self.table = ttk.Treeview(self)
        self.__setup_table()
        self.__display_public_rooms()
        for _ in range(50):
            self.insert_new_row([None, None, None, None, None])
        self.table.pack(fill='both')

    def __setup_table(self):
        self.table.tag_configure('row', background='gray')
        self.table['columns'] = ('id', 'server_ip', 'server_port', 'name', 'keeps_logs')
        self.table.column("#0", width=0, stretch='no')
        self.table.column("id", anchor="center", width=100)
        self.table.column("server_ip", anchor="center", width=100)
        self.table.column("server_port", anchor="center", width=100)
        self.table.column("name", anchor="center", width=100)
        self.table.column("keeps_logs", anchor="center", width=100)

        self.table.heading("#0", text="", anchor='center')
        self.table.heading("id", text="ID", anchor='center')
        self.table.heading("server_port", text="port", anchor='center')
        self.table.heading("server_ip", text="ip", anchor='center')
        self.table.heading("name", text="name", anchor='center')
        self.table.heading("keeps_logs", text="keeps logs", anchor='center')

    def __display_public_rooms(self):
        rooms = get_public_rooms()
        for room in rooms:
            self.insert_new_row(room)
        

    def insert_new_row(self, room):
        id = room[0]
        serv_ip = room[1]
        serv_port = room[2]
        name = room[3]
        keeps_logs = room[4]
        self.table.insert(
            parent='', 
            index='end', 
            values=(id, serv_ip, serv_port, name, keeps_logs),
            tags=('row',)
        )
        

        