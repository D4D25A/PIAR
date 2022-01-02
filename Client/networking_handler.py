from nacl.public import PrivateKey, Box
from nacl.utils import EncryptedMessage

import threading
import logging
import socket
import pickle

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

    @staticmethod 
    def acknowledge_invaild_userame(client_obj):
        data = pickle.dumps({'command':12})
        client_obj.s.send(data)

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
        self.username_unique = "nothing"
        self.connected = False

    def connect_to_room(self):
        try:
            self.s.connect((self.room_ip, self.room_port))
            self.connected = True
            return 1
        except (socket.error, pickle.PickleError) as e:
            print("There was an exception...")
            print(e)
            self.connected = False
            return 0

    def start_listening_for_data(self):
        self.data_listener_tr = threading.Thread(target=self.listen_for_data)
        self.data_listener_tr.start()

    def new_box(self, public_key) -> Box:
        return Box(self.private_key, public_key)

    def verify_unique_username(self):
        Commands.verify_unique_username(self, self.username)

    def relay_msg(self, msg:str):
        for username, public_key in self.clients.items():
            enc_msg = self.new_box(public_key).encrypt(bytes(msg, 'utf-8'))
            Commands.send_server_enc_msg(self, enc_msg, username, self.public_key)

    def wait_for_username_verification(self):
        while self.username_unique == "nothing":
            continue
        return 1 if self.username_unique else 0

    def send_creds(self):
        Commands.send_creds_to_server(
            self, 
            self.username, 
            self.public_key
        )

    def listen_for_data(self):
        while self.connected:
            try:
                data = self.s.recv(self.BUFFER_SIZE)
                print(f"Recieved data...")
                
                if data == b"":
                    self.on_server_shutdown()

                data = pickle.loads(data)

                # encrypted msg from server
                if data['command'] == 2:
                    enc_msg = data['enc_msg']
                    public_key = data['public_key']
                    box = self.new_box(public_key)
                    msg = box.decrypt(enc_msg).decode('utf-8')
                    
                    self.room_UI.render_new_msg(msg)
                
                # username unique response
                if data['command'] == 5:
                    print("Recieved code 5 from the server")
                    if data['res'] == "OK":
                        print("Setting username unique to true")
                        self.username_unique = True 
                    else:
                        print("Response was NO")
                        self.username_unique = False

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

            except (socket.error, ) as e:
                logging.error(e)
                self.connected = False
                self.on_server_shutdown()

    def on_disconnect(self):
        pass

    def on_server_shutdown(self):
        self.room_UI.render_new_msg("Lost connection to server. Most likely the server went offline!", 'red')


if __name__ == '__main__':
    client = RoomBackgroundHandler("192.168.0.68", 4444, 'billyb0b')
    client.connect_to_room()