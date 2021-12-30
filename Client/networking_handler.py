def new_room(id, serv_ip, serv_port, name, keeps_logs):
        """Returns an array for the room

        Args:
            id (int): unique ID for the room. 
            serv_ip (str): server ip for the room
            serv_port (int): server port for the room
            name (str): name of the room
            keeps_logs (bool): boolean value to know if the owner keeps logs

        Returns:
            array: for the data to be easily put into a treeview
        """
        return [id, serv_ip, serv_port, name, keeps_logs]

def get_public_rooms():
    r1 = new_room(1, "192.168.0.0", 4444, "waterparks", False)
    r2 = new_room(2, "192.168.0.0", 4444, "dogs", False)
    r3 = new_room(3, "192.168.0.0", 4444, "cats", False)
    r4 = new_room(4, "192.168.0.0", 4444, "programming", False)
    return [r1, r2, r3, r4]