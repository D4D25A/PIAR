from nacl.public import PrivateKey, Box
from nacl.utils import EncryptedMessage

class EncryptionHandler:
    def __init__(self):
        self.__generate_new_keys()
    
    def __generate_new_keys(self):
        self.private_key = PrivateKey.generate()
        self.public_key = self.private_key.public_key

    def new_box_with_server(self, server_public_key):
        self.box = Box(self.private_key, server_public_key)

    def encrypt_msg(self, msg) -> EncryptedMessage:
        return self.box.encrypt(msg)

    # this is called when the room is disconnected
    def __delete__(self):
        del self

    def __hash__(self):
        return hash(self)