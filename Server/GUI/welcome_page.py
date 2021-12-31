from tkinter import Frame, scrolledtext

import os
from tkinter.constants import WORD

class Welcome(Frame):
    def __init__(self):
        super().__init__()
        self.text = scrolledtext.ScrolledText(self, wrap=WORD)
        self.__open_welcome_file()

    def __insert_welcome_text(self, text):
        self.text.config(state='normal')
        self.text.insert('end', text)
        self.text.config(state='disabled')

    def __open_welcome_file(self):
        with open('Server/GUI/welcome.txt') as f:
            data = f.read()
            self.__insert_welcome_text(data)
