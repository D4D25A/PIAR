from nacl.public import PrivateKey, Box
from nacl.utils import EncryptedMessage

import threading
import socket
import pickle
import time

class Commands:
    @staticmethod
    def send_server_enc_msg(client_obj, enc_msg:EncryptedMessage):
        data = pickle.dumps({'id':1, 'enc_msg':enc_msg})
        client_obj.s.send(data)

    @staticmethod
    def send_creds_to_server(client_obj, username, public_key):
        data = pickle.dumps({'id':6, 'username':username, 'public_key':public_key})
        client_obj.s.send(data)

    @staticmethod
    def get_all_connected_clients(client_obj):
        data = pickle.dumps({'id':4})
        client_obj.send(data)
    
class RoomBackgroundHandler:
    # 5 kb of data
    BUFFER_SIZE = 5 * 1024

    # Just pass chat room gui class here?
    def __init__(self, room_UI, room_ip:str, room_port:int, username:str):
        """This handles all the networking and encryption for the room.

        Args:
            room_UI (ChatRoomUIHandler): The frontend UI class object
            room_ip (str): The room host IP
            room_port (int): The room host Port
            username (str): The client's username
        """
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username
        print(self.username)
        self.room_ip = room_ip
        self.room_port = room_port
        self.room_UI = room_UI
        self._private_key = PrivateKey.generate()
        self._public_key = self._private_key.public_key
        self._box:Box = None

    def connect_to_room(self):
        try:
            self.s.connect((self.room_ip, self.room_port))
            print("Connected to server...")
            self.connected = True
            return 1
        except socket.error as e:
            print("There was an exception...")
            print(e)
            return 0

    def connected(self) -> bool:
        print("Checking if connected")
        try:
            self.s.send(b"")
        except socket.error:
            print("Not connected to server!")
            self.connected = False
            self.connect_to_room()

    def listen_for_data(self):
        while self.connected:
            try:
                if data == b"":
                    self.on_disconnect()

                data = self.sock_obj.recv(self.BUFFER_SIZE)
                data = pickle.loads(data)

                # encrypted msg from server
                if data['commmand'] == 2:
                    if self._box:
                        enc_msg = data['enc_msg']
                        self._box.decrypt(enc_msg)
                        pass
                    print("Recieved an encrypted message but no box is available")
                
                # public key sent form server
                elif data['command'] == 7:
                    s_pub_key = data['public_key']
                    self.on_request_new_box(s_pub_key)

            except Exception as e:
                print(e)
                self.connected = False
        else:
            self.on_disconnect()

    def send_command_to_server(self, cmd):
        try:
            data = pickle.dumps(cmd)
            self.s.send(data)
        except Exception as e:
            print("An error occured sending the cmd")
            print(e)

    def on_disconnect(self):
        # render "connected to server has been lost!"
        self.connected = False
        del self

    # ----------------------- EVENTS -----------------------
    def on_request_new_box(self, server_public_key):
        self.new_box(server_public_key)

    def encrypt_msg(self, msg:str) -> EncryptedMessage:
        pass

    def decrypt_msg(self, EncryptedMessage) -> str:
        pass

    # ----------------------- Getters -----------------------
    def __private_key__(self):
        return self._private_key

    def __public_key__(self):
        return self._public_key
    
    def __get_box__(self):
        return self._box

    # ----------------------- Setters -----------------------
    def set_private_key(self, private_key):
        self._private_key = private_key
    
    def set_public_key(self, public_key):
        self._public_key = public_key

    def new_box(self, room_public_key):
        self._box = Box(self.__private_key__(), room_public_key)

if __name__ == '__main__':
    client = RoomBackgroundHandler("192.168.0.68", 4444, 'billyb0b')
    client.connect_to_room()