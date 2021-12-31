from tkinter import Button, Entry, Toplevel, messagebox

class UsernameEntry(Toplevel):
    def __init__(self, w:int, h:int, title:str):
        self.username_ok = False
        super().__init__()
        self.geometry(f"{w}x{h}")
        self.wm_title(title)
        self.__create_entry_widget()
        self.__create_ok_button()

    def __create_entry_widget(self):
        self.entry = Entry(self)
        self.entry.pack()

    def __create_ok_button(self):
        self.ok_btn = Button(self, text='Submit', command=self.__on_submit_pressed)
        self.ok_btn.pack()

    def __on_submit_pressed(self):
        self.username = self.entry.get()
        if len(self.username) < 4:
            messagebox.showerror('Username Error', 'The length of the username must be more than 4 or more')
        elif len(self.username) > 10:
            messagebox.showerror('Username Error', 'The length of the username 10 or less')
        self.username_ok = True
        self.destroy()
    
    def get_username(self):
        return self.username
