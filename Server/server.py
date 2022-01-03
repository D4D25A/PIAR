import threading
import logging
import random
import socket
import pickle
import string
import time
import os

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
        self.room = room_server
        self.client_sock = client_sock_obj
        self.public_key = None
        self.connected = True
        self.username = None
        self.alive = True
        self.id = self.generate_random_id()

    def run(self):
        while True:
            try:
                self.listen_for_data()
            except Exception as e:
                print("An exception as occured")
                logging.error(e)
                self.on_disconnect()

    def generate_random_id(self):
        legal_chars = string.ascii_letters + string.digits
        return "".join(random.choice(legal_chars) for _ in range(40))
    
    def listen_for_data(self):
        print("Listening for data...")
        data = self.client_sock.recv(self.BUFFER_SIZE)
        data = pickle.loads(data)

        # encrypted message from client
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
                    print(f"Sending command 2 to {to}")
                    # print(f"Relayed the message to {client.username}...")
                    break

            # verify username
        elif data['command'] == 3:
            res = {'command':5}
            for client in self.room.clients:
                if client.username == data['username']:
                    print("Res is no!")
                    res['res'] = "NO"
                    break
                res['res'] = "OK"

            print("Sending response 5...")
            data = pickle.dumps(res)
            print(f"Sending the res {res}")
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

        # acknowledge bad username (close self)
        elif data['command'] == 12:
            print("Recieved acknowledgement from client!")
            self.on_disconnect(broadcast=False)

        else:
            print(data)

    def on_disconnect(self, broadcast=True):
        print("On disconnect called.")
        self.alive = False
        self.client_sock.shutdown(socket.SHUT_RDWR)
        self.client_sock.close()
        self.room.remove_client(self.id)
        if broadcast:
            print("Broadcasting")
            self.room.on_user_disconnect(self.username)

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
                c.start()
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

    def remove_client(self, id):
        for i, client in enumerate(self.clients):
            if client.id == id:
                del self.clients[i]
                return 1
        return 0

def main():
    if os.name == "nt":
        os.system('cls')
    elif os.name == "posix":
        os.system('clear')
    else:
        print("Unknown os!")

    server_ip = str(input("Enter the server ip: "))
    server_port = int(input("Enter the server port: "))
    s = Listener(server_ip, server_port)
    thread = threading.Thread(target=s.listen_for_connections)
    thread.start()

if __name__ == '__main__':
    main()