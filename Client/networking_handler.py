import socket
import pickle

# for testing
import string
import random
#############

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
    def random_room_id(max_len:int):
        vaild_chars = string.ascii_letters + string.octdigits
        return "".join(random.choice(vaild_chars) for _ in range(max_len))
    r1 = new_room(random_room_id(12), "192.168.0.0", 4444, "waterparks", False)
    r2 = new_room(random_room_id(12), "192.168.0.0", 4445, "dogs", False)
    r3 = new_room(random_room_id(12), "192.168.0.0", 4446, "cats", False)
    r4 = new_room(random_room_id(12), "192.168.0.0", 4447, "programming", False)
    r4 = new_room(random_room_id(12), "192.168.0.0", 4447, "programming", False)
    r4 = new_room(random_room_id(12), "192.168.0.0", 4447, "programming", False)
    return [r1, r2, r3, r4]

class RoomConnectionHandler:
    def __init__(self, ip:str, port:int, username:str, disconnect_callback):
        """The connection handler for a room. Client -> Server
        Args:
            ip (str): the ip of the room
            port (int): the port of the room
            username (str): the user's username that they put
            failure_callback (function): disconnect_callback
        """
        self.disconnect_callback = disconnect_callback
        self.s = None
        self.username = username
        self.connected = True
        self.port = port
        self.ip = ip

        self.__initalize_sock()

    def __initalize_sock(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.ip, self.port))
        except (socket.error,) as e:
            print("Failed to connect to room server...")
            print(e.strerror)

    def connected(self):
        try:
            self.s.send("hello")
            return True
        except (socket.error,) as e:
            print("Exception occurred...")
            print(e.strerror)
            return False


    def __send_data_to_room(self, id, data):
        try:
            if self.connected():
                pickld_data = pickle.dumps({'command':id, 'data':data})
                self.s.send(pickld_data)
                return 1
        except (socket.error, Exception) as e:
            print("An error has occured...")
            print(e.with_traceback())
            return e

    # need to put this in a thread
    def __listen_for_data(self, buffer_size:int):
        try:
            while True:
                data = self.s.recv(buffer_size)
                data = pickle.loads(data)

                if data['command'] == 1:
                    pass

        except Exception as e:
            print("An exception has occured...")
            print(e)

    def send_enc_msg(self, enc_msg):
        self.__send_data_to_room(1, enc_msg)
        

    def __on_disconnect(self):
        self.disconnect_callback()

    def __get_sock__(self):
        return self.s