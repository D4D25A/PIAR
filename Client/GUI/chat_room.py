from tkinter import Entry, Frame, LabelFrame, Label
from tkinter.scrolledtext import ScrolledText
from time_funcs import Time


# just for abstraction
class ScrollPanel(ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(state='disabled')
        self.__configure_tags()

    def __configure_tags(self):
        self.tag_configure('error', foreground='red')
        self.tag_configure('success', foreground='green')

    # tag is None just for dev phase
    def render_new_txt(self, text, tag=None):
        self.config(state ='normal')
        self.insert('end', f"{text}\n", tag)
        self.see('end')
        self.config(state = 'disabled')
    
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
    def __init__(self, room_connection_obj, encryption_obj):
        super().__init__()
        self.networking_obj = room_connection_obj
        self.encryption_obj = encryption_obj    


        # the username_panel will most likely become a tree view
        # as it just lists all the connected users. Much more
        # efficient to use a tree view
        self.username_panel = ScrollPanel(self, width=15)
        self.textbox = ScrollPanel(self)
        self.entry_widget = EntryPanel(self)

        self.entry_widget.pack(side='bottom', fill='x', anchor='s')
        self.username_panel.pack(side='right', fill='y', anchor='w')
        self.textbox.pack(expand=1, fill="both")

    def __send_msg_to_server(self, msg):
        enc_msg = self.encryption_obj.encrypt_msg(msg)
        status = self.networking_obj.send_enc_msg(enc_msg)
        if status != 1:
            self.__render_new_text('SERVER ERROR', status)

    def __render_new_text(self, username:str, msg:str):
        """Render some text to the chat room main ScrolledText widget

        Args:
            username (str): The username
            msg (str): The message/text to be rendered
        """
        text = f"<{username}> - {msg}"
        self.textbox.render_new_txt(text, tag='error')

    def __get_room_connection_obj__(self):
        return self.networking_obj

    def __get_room_connection_obj_sock__(self):
        return self.networking_obj.__get_sock__()