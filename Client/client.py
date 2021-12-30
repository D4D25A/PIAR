from GUI import welcome_window, root_window, public_servers, chat_room

if __name__ == '__main__':
    root_window = root_window.RootWindow(1200, 800)
    
    # this tab is just for testing
    chat_room_window = chat_room.RootFrame()
    root_window.add_new_tab(chat_room_window, "debug room")
    ##########################################################

    public_rooms_frame = public_servers.PublicServersFrame()
    root_window.add_new_tab(public_rooms_frame, "Public Rooms")

    root_window.mainloop()