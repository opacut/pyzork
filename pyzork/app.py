import json

FILE_PATH = 'rooms.json'
ACTION_VERBS = ['go','move','look','inspect','take','open','close','push','pull','pick','talk']
COMBINATION_VERBS = ['give','use','put']
INSPECT_VERBS = ['look','inspect']
NORTH_STRINGS = ['n','north','notrh']
WEST_STRINGS = ['w','west','wset']
SOUTH_STRINGS = ['s','south','sotuh']
EAST_STRINGS = ['e','east','esat']
SORRY_STRING = 'I\'m sorry, I didn\'t catch that.'
MOVE_VERBS = ['go','move']
CANNOT_TAKE = "There is no such item here for you to take."
EXIT_CODES = {
    'n':0,
    'w':1,
    's':2,
    'e':3
}


class GameState:
    def __init__(self):
        self.rooms = self.get_rooms_from_file(FILE_PATH)
        self.current_room = None
        self.change_current_room('Entrance')
        self.loop = True
        self.parser = Parser(self)
        self.inventory = list()

    def get_rooms_from_file(self, file_path):
        rooms = list()
        with open(file_path) as rooms_file:
            data = json.load(rooms_file)
            for d in data:
                rooms.append(Room(d))
        return rooms

    def change_current_room(self,room_name):
        self.current_room = next(room for room in self.rooms if room['name']==room_name)

    def quit_game(self):
        self.loop = False

    def move(self,direction):
        index = EXIT_CODES[direction]
        self.change_current_room(self.current_room.exits[index])

    def take(self, item):
        if item in self.current_room.items:
            self.inventory.append(item)
            self.current_room.items.remove(item)
        else:
            print(CANNOT_TAKE)
    
    def inspect(self):
        print(self.current_room.description)

    def sorry(self):
        print(SORRY_STRING)
    
    def look_at(self,item):
        if item in self.current_room.items:
            self.inventory.append(item)
            self.current_room.items.remove(item)
        else:
            print(CANNOT_TAKE)

    def open(self,item):
        #open item in room or inventory
        pass

    def close(self,item):
        #close item in room or inventory
        pass

    def read(self,item):
        #read item in room or inventory
        pass

    def push(self,item):
        #push item in room
        pass

    def pull(self,item):
        #pull item in room or inventory
        pass

    def pick(self,item):
        #pick up item in room or inventory
        pass

    def talk(self,item):
        #talk to item in room or inventory
        pass

    def give(self,item):
        #talk to item in room or inventory
        pass

    def use(self,item):
        #talk to item in room or inventory
        pass

    def put(self,item):
        #talk to item in room or inventory
        pass




class Item:
    def __init__(self,item_data,gs=None):
        self.game_state = gs
        self.name = item_data['name']
        self.description = item_data['description']
        self.description_inventory = item_data['description_inventory']
    
    def combine(self,second_item):
        #combine the two items
        pass


class Parser:
    def __init__(self,gs):
        self.game_state = gs

    def parse(self,inp):
        inp = inp.upper().lower()
        inp_split = inp.split()
        #if len(inp_split) == 1:
        if inp_split[0] == 'look':
            if inp_split[1]=='around':
                self.game_state.inspect()
            else:
                self.game_state.look_at(inp_split[-1])
        elif inp_split[0] in NORTH_STRINGS:
            self.game_state.move('n')
        elif inp_split[0] in WEST_STRINGS:
            self.game_state.move('w')
        elif inp_split[0] in SOUTH_STRINGS:
            self.game_state.move('s')
        elif inp_split[0] in EAST_STRINGS:
            self.game_state.move('e')
        elif inp_split[0] in MOVE_VERBS:
            self.parse(str(inp_split[1:]))
        elif inp_split[0] == 'take':
            self.game_state.take(inp_split[-1])
        elif inp_split[0] == 'open':
            self.game_state.open(inp_split[-1])
        elif inp_split[0] == 'close':
            self.game_state.close(inp_split[-1])
        elif inp_split[0] == 'read':
            self.game_state.read(inp_split[-1])
        elif inp_split[0] == 'push':
            self.game_state.push(inp_split[-1])
        elif inp_split[0] == 'pull':
            self.game_state.pull(inp_split[-1])
        elif inp_split[0] == 'pick':
            self.game_state.pick(inp_split[-1])
        elif inp_split[0] == 'talk':
            self.game_state.talk(inp_split[-1])
        #these need more
        elif inp_split[0] == 'give':
            self.game_state.give(inp_split[1],inp_split[3])
        elif inp_split[0] == 'use':
            self.game_state.give(inp_split[1],inp_split[3])
        elif inp_split[0] == 'put':
            self.game_state.give(inp_split[1],inp_split[3])
        else:
            self.game_state.sorry()
        
class Room:
    def __init__(self, room_data,gs=None):
        self.name = room_data['name']
        self.description = room_data['description']
        self.exits = room_data['exits']
        self.game_state = gs
        self.special = room_data['special']
        self.items = room_data['items']




game_state = GameState()
print("Welcome to Zork!")
while(game_state.loop):
    print()
    print(game_state.current_room.description)
    inp = input("What would you like to do next?\n")

    game_state.current_room.exit(inp)
