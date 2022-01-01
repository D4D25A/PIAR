from tkinter import Button, Entry, Toplevel, messagebox

class UsernameEntry(Toplevel):
    def __init__(self, w:int, h:int, title:str):
        super().__init__()
        self.geometry(f"{w}x{h}")
        self.wm_title(title)
        self.__create_entry_widget()
        self.__create_ok_button()
        self.username = None
        self.username_ok = False

    def __create_entry_widget(self):
        self.entry = Entry(self)
        self.entry.pack()

    def __create_ok_button(self):
        self.ok_btn = Button(self, text='Submit', command=self.__on_submit_pressed)
        self.ok_btn.pack()

    def __on_submit_pressed(self):
        username = self.entry.get()
        if len(username) < 4:
            messagebox.showerror('Username Error', 'The length of the username must be more than 4 or more')
            self.username_ok = False
            return
        elif len(username) > 10:
            messagebox.showerror('Username Error', 'The length of the username 10 or less')
            self.username_ok = False
            return

        self.username = username
        self.username_ok = True
        self.destroy()

