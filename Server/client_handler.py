from socket import socket

import threading
import pickle

class Client(threading.Thread):
    # 5 kb of data
    BUFFER_SIZE = 5 * 1024

    def __init__(self, sock_obj:socket):
        super().__init__(self, target=self.__client_listener)
        self.sock_obj = sock_obj
        self.not_disconnected = True

    def __listen_for_data(self):
        while self.not_disconnected:
            data = self.sock_obj.recv(self.BUFFER_SIZE)
            data = pickle.loads(data)

            # the data will be the dict object.
            # for example, {'command':COMMAND_ID, 'data':DATA}
            # data if needed

            if data['command'] == 1:
                pass
            
            elif data['command'] == 2:
                pass
            
            elif data['command'] == 3:
                pass
            
            elif data['command'] == 4:
                pass
            
            elif data['command'] == 5:
                pass
            
            elif data['command'] == 6:
                pass
