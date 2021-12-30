import random
import string

class Room:
    def __init__(self):
        self.room_id = self.__generate_room_id(12)
        print(self.room_id)
    
    def __generate_room_id(self, max_len:int):
        vaild_chars = string.ascii_letters + string.octdigits
        return "".join(random.choice(vaild_chars) for _ in range(max_len))

    def __room_id__(self) -> str:
        return self.room_id

class RoomHandler:
    def __init__(self):
        self.rooms = []
    
    def new_room(self):
        pass

if __name__ == '__main__':
    print(Room().__room_id__())