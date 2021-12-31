from tkinter import Frame, ttk


class PublicServersFrame(Frame):
    def __init__(self, root):
        self.root = root

        super().__init__(background='red')
        self.table = ttk.Treeview(self)
        self.__setup_table()
        self.__display_public_rooms()
        self.table.pack(expand=1, fill='both')
        self.table.bind('<Double-Button-1>', self.__on_double_click)

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
        rooms = [['gsg234A', '192.168.0.68', 4444, 'programming', False]]
        for room in rooms:
            self.insert_new_row(room)
    
    def __on_double_click(self, event):
        item_id = event.widget.focus()
        item = event.widget.item(item_id)
        values = item['values']
        ip, port= values[1], values[2]
        self.root.connect_to_room(ip, port)

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
        

        