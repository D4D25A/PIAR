import socket
import pickle
import _thread
import time

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
        

class AbstractNetworking:
    def __init__(self, ip:str, port:int, disconnect_callback):
        """The connection handler for a room. Client -> Server
        Args:
            ip (str): the ip of the room
            port (int): the port of the room
            failure_callback (function): disconnect_callback
        """
        self.disconnect_callback = disconnect_callback
        self.s = None
        self.connected = True
        self.port = port
        self.ip = ip
        self.threads = []

    def initalize_sock(self, err_msg=None):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.ip, self.port))
            return 1
        except (socket.error,) as e:
            print("Failed to connect to server")
            print(e.strerror)
            return 0

    def connected(self):
        try:
            self.s.send("hello")
            return True
        except (socket.error,) as e:
            print("Exception occurred...")
            print(e.strerror)
            return False


    def send_data_to_server(self, id, data):
        try:
            if self.connected():
                pickld_data = pickle.dumps({'command':id, 'data':data})
                self.s.send(pickld_data)
                return 1
        except (socket.error, Exception) as e:
            print("An error has occured...")
            print(e.with_traceback())
            return e

    def new_listen_for_data_thread(self):
        tr = _thread.start_new_thread(self.listen_for_data, (2048,))
        self.threads.append(tr)

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
        
    def reconnect(self):
        pass

    def __on_disconnect(self):
        self.disconnect_callback()

    def __get_sock__(self):
        return self.s

class RoomHandler(AbstractNetworking):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect_to_room(self) -> int:
        return self.initalize_sock()
        

class MainServerConnectionHandler(AbstractNetworking):
    def __init__(self):
        super().__init__("192.168.0.68", 4444, self.__on_disconnect)
    
    def connect_to_master_server(self):
        status = 0
        while not status:
            status = self.initalize_sock()
            time.sleep(2)

    def __on_disconnect(self):
        pass