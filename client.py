from Client.root_window import RootWindow, on_exit

if __name__ == '__main__':
    root = RootWindow(1200, 800, )
    root.protocol("WM_DELETE_WINDOW", on_exit)
    root.mainloop()