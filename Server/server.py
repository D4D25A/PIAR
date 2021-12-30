"""
The server needs to listen for commands and return a response. Simple right?
The commands will be from sent in the form of new_command_to_server({'cmd':COMMAND_ID}) from 
the client and the server will send back new_command_to_client({'cmd':COMMAND_ID, 'data': RES_DATA}) 
and vice versa.
"""

from client_handler import Client
from room_handler import *

class Server:
    def __init__(self, listen_ip, listen_port):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        