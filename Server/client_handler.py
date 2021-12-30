import threading

class Client(threading.Thread):
    def __init__(self):
        super().__init__(self, target=self.__client_listener)
