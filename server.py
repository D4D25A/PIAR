from Server.rooms_handler import Listener
import threading
import os

if __name__ == '__main__':
    if os.name == "nt":
        os.system('cls')
    elif os.name == "posix":
        os.system('clear')
    else:
        print("Unknown os!")
        exit()

    server_ip = str(input("Enter the server ip: "))
    server_port = int(input("Enter the server port: "))
    s = Listener(server_ip, server_port)
    thread = threading.Thread(target=s.listen_for_connections)
    thread.start()
