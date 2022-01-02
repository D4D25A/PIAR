from nacl.public import PrivateKey, Box
from nacl.utils import EncryptedMessage
import _thread as thread
import threading
import logging
import socket
import pickle
import time


class Client:
    # 5 kb of data
    BUFFER_SIZE = 5 * 1024

    def __init__(self, client_sock_obj, room_server):
        """Server side Client handler
        Args:
            client_obj (client from accept()): client object
            room_server (room_handler [Listener]): room main server
        """
        self.room = room_server
        self.client_sock = client_sock_obj
        self.public_key = None
        self.connected = True
        self.username = None
        self.alive = True

    def listen_for_data(self):
        # msg = f"<{self.username}> has joined the chat!"
        # self.room.broadcast_data({'command':9, 'msg':msg})
        # print("Listening for data...")
        while self.connected:
            try:
                data = self.client_sock.recv(self.BUFFER_SIZE)
                data = pickle.loads(data)

                # encrypted message from client
                # broadcasts the message to all 
                # the other connected sockets
                if data['command'] == 1:
                    to = data['to']
                    enc_msg = data['enc_msg']
                    public_key = data['public_key']
                    # print(data)
                    for client in self.room.clients:
                        if client.username == to:
                            pckld_data = pickle.dumps({
                                'command':2,
                                'to':to, 
                                'enc_msg':enc_msg, 
                                'public_key':public_key
                            })
                            client.client_sock.send(pckld_data)
                            # print(f"Relayed the message to {client.username}...")
                            break

                # verify username
                elif data['command'] == 3:
                    res = {'command':5}
                    for client in self.room.clients:
                        if client.username == data['username']:
                            res['res'] = "NO"
                            self.on_disconnect()
                            return
                    else:
                        res['res'] = "OK"
                    # print("Sending response 5...")
                    # print(res)
                    data = pickle.dumps(res)
                    self.client_sock.send(data)

                # client senting creds
                elif data['command'] == 6:
                    self.username = data['username']
                    self.public_key = data['public_key']
                    # print("Recieved code 6 from client")
                    # print(data)
                    # print(self.username, self.public_key)
                    # self.room.clients[self.username] = self.public_key
                    self.room.broadcast_new_user_list()

                else:
                    continue
            except Exception as e:
                logging.error(e)
                self.on_disconnect()

    def on_disconnect(self):
        self.room.on_user_disconnect(self.username)
        self.client_sock.close()
        self.alive = False
        self.room.clients.pop(self.room.clients.index(self))
        # print(self.room.clients)
        del self

    def get_creds(self):
        return {self.username: self.public_key}


class Listener:
    BUFFER_SIZE = 5 * 1024

    def __init__(self, listen_ip, listen_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_port = listen_port
        self.listen_ip = listen_ip
        self.clients = []

        self.sock_config()
        # self.listen_for_connections()

    def sock_config(self):
        while True:
            try:
                print("Trying to bind...")
                self.s.bind((self.listen_ip, self.listen_port))
                print("Binded...")
                break
            except:
                time.sleep(2)
                continue
        self.s.listen()

    def listen_for_connections(self):
        print(f"Room listening on {self.listen_ip}:{self.listen_port}")
        try:
            while True:
                client_obj, addr = self.s.accept()
                print("Recieved new client req!")
                c = Client(client_obj, self)
                c_tr = threading.Thread(target=c.listen_for_data)
                c_tr.start()
                self.clients.append(c)
                print("Created and started a new thread for the client req... Listening again!")
        except socket.error as e:
            print("There was an error...")
            print(e)

    def broadcast_new_user_list(self):
        new_creds = {}
        for client in self.clients:
            new_creds[client.username] = client.public_key
        # print(f"new_creds: {new_creds}")
        self.broadcast_data({'command':11, 'creds':new_creds})

    def on_user_disconnect(self, username):
        msg = f"<{username}> has disconnected from the chat!"
        self.broadcast_data({'command':10, 'msg':msg})
        self.broadcast_new_user_list()

    def broadcast_data(self, data):
        pckld_data = pickle.dumps(data)
        for client in self.clients:
            client.client_sock.send(pckld_data)

if __name__ == '__main__':
    s = Listener("192.168.0.68", 4444)
    thread = threading.Thread(target=s.listen_for_connections)
    thread.start()
