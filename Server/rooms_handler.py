from nacl.public import PrivateKey, Box
from nacl.utils import EncryptedMessage
import threading
import socket
import pickle
import time

class Client(threading.Thread):
    # 5 kb of data
    BUFFER_SIZE = 5 * 1024

    def __init__(self, client_sock_obj, room_server):
        """Server side Client handler
        Args:
            client_obj (client from accept()): client object
            room_server (room_handler [Listener]): room main server
        """
        threading.Thread.__init__(self)
        self.room_server = room_server
        self.client_sock = client_sock_obj
        self.client_public_key = None
        self.client_username = None
        self.box:Box = None
        self.connected = True

    def run(self):
        self.listen_for_data()

    def listen_for_data(self):
        print("Listening for data...")
        while self.connected:
            try:
                data = self.client_sock.recv(self.BUFFER_SIZE)
                data = pickle.loads(data)

                # encrypted msg from client
                if data['command'] == 1:
                    print("Recieved encrypted msg from client")
                    pckld_msg = data['enc_msg']
                    enc_msg = pickle.loads(pckld_msg)
                    self.room_server.on_recv_msg(enc_msg)

                # verify unique username
                if data['command'] == 3:
                    username = data['username']
                    if username in self.room_server.keys:
                        print("Sending response NOT UNIQUE")
                        self.client_sock.send('NOT UNIQUE'.encode('ascii'))
                    else:
                        print("sending response OK")
                        self.client_sock.send('OK'.encode('ascii'))

                # get all users in the room
                if data['command'] == 4:
                    pass
                
                # creds of the client (public_key and username)
                if data['command'] == 6:
                    username, self.client_public_key = data['username'], data['public_key']
                    # create a box
                    self.box = Box(self.room_server.private_key, self.client_public_key)



                # client sending public key here
                if data['command'] == 9:
                    pass
                    
            except Exception as e:
                print(e)
                self.connected = False
        else:
            self.on_disconnect()

    def on_disconnect(self):
        print("on_disconnect called!")
        del self

    def decrypt_msg(self, enc_msg:EncryptedMessage):
        """Decrypts an encrypted message from the client to be
        fowarded on

        Args:
            enc_msg (EncryptedMessage): Encrypted message object

        Returns:
            str: plaintext of the ciphertext
        """

        return self.box.decrypt(enc_msg)

    def send_new_msg(self, msg:str):
        """Sends an encrypted message to the client

        Args:
            msg (str): Message in plaintext
        """
        enc_msg = self.box.encrypt(bytes(msg, 'utf-8'))
        data = {'command':2, 'enc_msg':enc_msg}
        data = pickle.dumps(data)
        self.client_sock.send(data)

class Listener:
    BUFFER_SIZE = 5 * 1024

    def __init__(self, listen_ip, listen_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.boxes = {}
        self.threads = []
        self.clients = []
        self.keys = {}
        self.listen_port = listen_port
        self.listen_ip = listen_ip
        self.private_key = PrivateKey.generate()
        self.public_key = self.private_key.public_key
        self.sock_config()
        self.start_new_thread(self.listen_for_connections)

    def sock_config(self):
        while True:
            try:
                time.sleep(5)
                print("Trying to bind...")
                self.s.bind((self.listen_ip, self.listen_port))
                print("Binded...")
                break
            except:
                continue
        self.s.listen()

    def start_new_thread(self, target):
        tr = threading.Thread(target=target)
        tr.start()
        tr.join()
        self.threads.append(tr)

    def listen_for_connections(self):
        print(f"Room listening on {self.listen_ip}:{self.listen_port}")
        try:
            while True:
                client_obj, addr = self.s.accept()
                c_tr = Client(client_obj, self)
                c_tr.start()
                self.clients.append(c_tr)
        except socket.error as e:
            print("There was an error...")
            print(e)

    def broadcast_msg(self):
        pass

if __name__ == '__main__':
    Listener("192.168.0.68", 4444)