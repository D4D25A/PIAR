from tkinter import Entry, Frame, LabelFrame, Label
from tkinter.scrolledtext import ScrolledText
from time_funcs import Time

# class UsernamePanel(ScrollWidgetsRoot):
#     def __init__(self, *args):
#         super().__init__(*args)
#         self.connected_clients = {}
    
#     def display_new_username(self, username):
#         time = Time.get_time_HMS()
#         widget = Label(self.username_panel, text=f"[{username}] ")
#         widget.pack()

#     def remove_displayed_username(self, username):
#         pass

# class ChatWindow(ScrollWidgetsRoot):
#     def __init__(self, root):
#         super().__init__(root)
#         self.config(state='disabled')

# just for abstraction
class ScrollPanel(ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(state='disabled')

    # tag is None just for dev phase
    def render_new_txt(self, text, tag=None):
        self.textbox['state'] = 'normal'
        self.textbox.insert('end', f"{text}\n", tag)
        self.textbox.see('end')
        self.textbox['state'] = 'disabled'
    
    def render_new_txt_as_label(self, text:str, root=None, **options):
        if not text.endswith("\n"):
            text += "\n"
        if root:
            label = Label(self, text=text, **options)
        else:
            label = Label(self, text=text, **options)

        label.pack()

class EntryPanel(Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initialize_static_options()

    def __initialize_static_options(self):
        self.bind('<Return>', self.__on_enter_pressed)
        self.pack(side='bottom', fill='x', anchor='s') 
    
    # gets the input and clears it 
    def __on_enter_pressed(self, msg):
        msg = self.get()
        self.delete(0, 'end')

class RootFrame(Frame):
    def __init__(self):
        super().__init__()
        
        # the username_panel will most likely become a tree view
        # as it just lists all the connected users. Much more
        # efficient to use a tree view
        self.username_panel = ScrollPanel(self, width=15)
        self.textbox = ScrollPanel(self)
        self.entry_widget = EntryPanel(self)

        self.entry_widget.pack(side='bottom', fill='x', anchor='s')
        self.username_panel.pack(side='right', fill='y', anchor='w')
        self.textbox.pack(expand=1, fill="both")

    def __display_msg_handler(self, username, msg):
        if len(msg) == 0:
            pass

        self.textbox.render_new_txt()


    def __send_msg_to_server(self, msg):
        pass

    def __on_recv_msg(self, username, msg):
        pass