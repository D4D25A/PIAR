import logging
from nacl.public import PrivateKey, Box
from nacl.utils import EncryptedMessage

import threading
import socket
import pickle
import time

class Commands:
    @staticmethod
    def send_server_enc_msg(client_obj, enc_msg:EncryptedMessage, to:str, public_key):
        data = pickle.dumps({'command':1, 'enc_msg':enc_msg, 'to':to, 'public_key':public_key})
        client_obj.s.send(data)
        print("sending encrypted msg to server!")

    @staticmethod
    def send_creds_to_server(client_obj, username, public_key):
        data = pickle.dumps({'command':6, 'username':username, 'public_key':public_key})
        client_obj.s.send(data)

    @staticmethod
    def verify_unique_username(client_obj, username):
        data = pickle.dumps({'command':3, 'username':username})
        client_obj.s.send(data)
    
    # @staticmethod
    # def request_other_users_creds(client_obj):
    #     data = pickle.dumps({})
    #     client_obj.s.send()
    
class RoomBackgroundHandler:
    # 5 kb of data
    BUFFER_SIZE = 5 * 1024

    # Just pass chat room gui class here?
    def __init__(self, room_UI, room_ip:str, room_port:int, username:str, username_verification_callback):
        """This handles all the networking and encryption for the room.

        Args:
            room_UI (ChatRoomUIHandler): The frontend UI class object
            room_ip (str): The room host IP
            room_port (int): The room host Port
            username (str): The client's username
        """

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_veri_call = username_verification_callback
        self.username = username
        self.room_ip = room_ip
        self.room_port = room_port
        self.room_UI = room_UI
        self.private_key = PrivateKey.generate()
        self.public_key = self.private_key.public_key
        self.clients = {}
        self.username_unique = False

        self.data_listener_tr = threading.Thread(target=self.listen_for_data)

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

    def verify_unique_username(self):
        Commands.verify_unique_username(self, self.username)

    def relay_msg(self, msg:str):
        print(self.clients.items())
        for username, public_key in self.clients.items():
            enc_msg = self.new_box(public_key).encrypt(bytes(msg, 'utf-8'))
            Commands.send_server_enc_msg(self, enc_msg, username, self.public_key)

    def listen_for_data(self):
        print("Listening for data...")
        while self.connected:
            try:
                data = self.s.recv(self.BUFFER_SIZE)
                
                if data == b"":
                    self.on_disconnect()

                data = pickle.loads(data)

                # encrypted msg from server
                if data['command'] == 2:
                    enc_msg = data['enc_msg']
                    public_key = data['public_key']
                    box = self.new_box(public_key)
                    msg = box.decrypt(enc_msg).decode('utf-8')
                    
                    # print(f"Encrypted msg: {enc_msg}")
                    # print(f"Decrypted msg: {msg}")
                    self.room_UI.render_new_msg(msg)
                
                # username unique response
                if data['command'] == 5:
                    print("Recieved code 5 from the server")
                    print(data)
                    if data['res'] == "OK":
                        print("Setting username unique to true")
                        self.username_unique = True
                    else:
                        self.username_unique = False
                    self.user_veri_call(self.username_unique)
                    print("Done")

                # public key sent from server
                elif data['command'] == 7:
                    print("Sent public key to server")
                    s_pub_key = data['public_key']
                    self.on_request_new_box(s_pub_key)

                # user connected to chat
                elif data['command'] == 9:
                    print("User connected to chat!")
                    msg = data['msg']
                    self.room_UI.render_new_msg(msg)

                # user disconnected from chat
                elif data['command'] == 10:
                    print("User disconnected from chat!")
                    msg = data['msg']
                    self.room_UI.render_new_msg(msg)

                # server sending creds
                elif data['command'] == 11:
                    print("Recieved code 11 from server!")
                    self.clients = data['creds']
                    print(self.clients)

            except Exception as e:
                logging.error(e)
                self.connected = False
        else:
            self.on_disconnect()

    def on_disconnect(self):
        # render "connected to server has been lost!" in message window
        # delete the tab also
        del self



if __name__ == '__main__':
    client = RoomBackgroundHandler("192.168.0.68", 4444, 'billyb0b')
    client.connect_to_room()