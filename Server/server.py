"""
The server needs to listen for commands and return a response. Simple right?
The commands will be from sent in the form of new_command_to_server({'cmd':COMMAND_ID}) from 
the client and the server will send back new_command_to_client({'cmd':COMMAND_ID, 'data': RES_DATA}) 
and vice versa.
"""
class Server:
    def __init__(self):
        pass