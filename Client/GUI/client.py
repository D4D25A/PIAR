from root_window import RootWindow
from public_servers import PublicServersFrame

if __name__ == '__main__':
    root_window = RootWindow(1200, 800)
    public_rooms_frame = PublicServersFrame()
    root_window.add_new_tab(public_rooms_frame, "Public Rooms")
    root_window.mainloop()