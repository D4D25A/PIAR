from nacl.public import PrivateKey, Box
from nacl.utils import EncryptedMessage

import threading
import socket
import pickle
import time

class Commands:
    @staticmethod
    def send_server_enc_msg(client_obj, enc_msg:EncryptedMessage, to:str, public_key):
        data = pickle.dumps({'id':1, 'enc_msg':enc_msg, 'to':to, 'public_key':public_key})
        client_obj.s.send(data)
        print("sending encrypted msg to server!")

    @staticmethod
    def send_creds_to_server(client_obj, username, public_key):
        data = pickle.dumps({'id':6})

    @staticmethod
    def request_other_users_creds(client_obj):
        data = pickle.dumps({})
    
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
        self.room_ip = room_ip
        self.room_port = room_port
        self.room_UI = room_UI
        self.private_key = PrivateKey.generate()
        self.public_key = self.private_key.public_key
        self.clients = {}

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

    def new_box(self, public_key) -> Box:
        return Box(self.private_key, public_key)

    def on_new_user_joined(self, username, public_key):
        clients[username] = public_key

    def on_new_user_left(self, username):
        del clients[username]

    def listen_for_data(self):
        while self.connected:
            try:
                if data == b"":
                    self.on_disconnect()

                data = self.sock_obj.recv(self.BUFFER_SIZE)
                data = pickle.loads(data)

                # encrypted msg from server
                if data['commmand'] == 2:
                    enc_msg = data['enc_msg']
                    public_key = data['public_key']
                    box = self.new_box(public_key)
                    msg = box.decrypt(enc_msg)
                    
                    print(f"Encrypted msg: {enc_msg}")
                    print(f"Decrypted msg: {msg}")
                    self.room_UI.render_new_msg(msg)
                    print("Recieved an encrypted message but no box is available")
                
                # public key sent form server
                elif data['command'] == 7:
                    s_pub_key = data['public_key']
                    self.on_request_new_box(s_pub_key)

                # user connected to chat
                elif data['command'] == 9:
                    msg = data['msg']
                    self.room_UI.render_new_msg(msg)

                # user disconnected from chat
                elif data['command'] == 10:
                    msg = data['msg']
                    self.room_UI.render_new_msg(msg)

                # server sending creds
                elif data['command'] == 11:
                    self.clients = data['creds']
                    print(self.clients)

            except Exception as e:
                print(e)
                self.connected = False
        else:
            self.on_disconnect()

    def on_disconnect(self):
        # render "connected to server has been lost!"
        self.connected = False
        del self

if __name__ == '__main__':
    client = RoomBackgroundHandler("192.168.0.68", 4444, 'billyb0b')
    client.connect_to_room()