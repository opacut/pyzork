import json

FILE_PATH = 'rooms.json'
ITEM_ATTRS_FILE_PATH = 'attributes.json'
ITEM_FILE_PATH = 'items.json'
ACTION_VERBS = ['go','move','look','inspect','take','open','close','push','pull','pick','talk']
COMBINATION_VERBS = ['give','use','put']
INSPECT_VERBS = ['look','inspect']
NORTH_STRINGS = ['n','north','notrh']
NORTH_NAME = "North"
NORTH_ABBREV = "n"
WEST_STRINGS = ['w','west','wset']
WEST_NAME = "West"
WEST_ABBREV = "w"
SOUTH_STRINGS = ['s','south','sotuh']
SOUTH_NAME = "South"
SOUTH_ABBREV = "s"
EAST_STRINGS = ['e','east','esat']
EAST_NAME = "East"
EAST_ABBREV = "e"
UP_STRINGS = ['u','up','upwards','upstairs']
UP_NAME = "Upstairs"
UP_ABBREV = "u"
DOWN_STRINGS = ['d','down','dwon','downwards','downstairs']
DOWN_NAME = "Downstairs"
DOWN_ABBREV = "d"
SORRY_STRING = "I'm sorry, I didn't catch that."
MOVE_VERBS = ['go','move']
CANNOT_TAKE = "There is no such item here for you to take."
CANNOT_EAT = "You can't eat that!"
CANNOT_USE = "That won't work."
CANNOT_LOOK = "There is no such item here."
LOCKED = "It's locked!"
TAKE_ITEM = "You take the %s."
STARTING_ROOM_PLAYER = 0 #"entrance"
STARTING_ROOM_MONSTER = 7 #"bedroom"
NO_EXIT = "There is no passage that way."
SEE_DOOR = "You can see doors leading to the %s to the %s."
INVENTORY_DESCRIPTION = "You are carrying: "
EMPTY_INVENTORY = "Your inventory is empty."
HAVE_NO_KEYS = "You don't have any keys!"
ALREADY_UNLOCKED = "That direction is already accessible!"
NO_SUCH_ITEM = "There is no such item in here."
WRONG_KEY = "The key doesn't fit!"
EXIT_CODES = {
    'n':0,
    'w':1,
    's':2,
    'e':3,
    'u':4,
    'd':5
}


class GameState:
    def __init__(self):
        self.rooms = self.get_rooms_from_file(FILE_PATH)
        self.item_attribute_pairs = self.get_item_attributes_from_file(ITEM_ATTRS_FILE_PATH)
        self.items_repository = self.get_items_from_file(ITEM_FILE_PATH)
        self.player_room = None
        self.change_current_room(STARTING_ROOM_PLAYER)
        self.loop = True
        self.parser = Parser(self)
        self.inventory = list()
        self.monster_room = STARTING_ROOM_MONSTER
        #self.room_index = self.build_rooms_index

    def move_monster(self,room_id):
        pass

    def execute(self,code):
        for s in code.split(";"):
            exec(s)

    def get_rooms_from_file(self, file_path):
        rooms = list()
        with open(file_path) as rooms_file:
            data = json.load(rooms_file)
            for d in data:
                rooms.append(Room(d,self))
        return rooms

    def get_item_attributes_from_file(self,file_path):
        #attributes = {}
        with open(file_path) as attr_file:
            data = json.load(attr_file)
        return data

    def get_items_from_file(self,file_path):
        items = list()
        with open(file_path) as items_file:
            data = json.load(items_file)
            for d in data:
                items.append(Item(d,self))
        return items

    def change_current_room(self,room_id):
        self.player_room = self.get_room_by_id(room_id)#next(room for room in self.rooms if room.name==room_name)

    def get_room_by_name(self,name):
        for room in self.rooms:
            if room.name.upper().lower() == name:
                return room
        return False

    def get_room_by_id(self,id):
        for room in self.rooms:
            if room.id == id:
                return room
        return False

    def quit_game(self):
        self.loop = False

    def add_item_to_room(self,item,room):
        self.get_room_by_name(room).items.add(item.id)

    def move(self,direction):
        #index = EXIT_CODES[direction]
        if direction in self.player_room.exits.keys():
            if direction in self.player_room.locked:
                print(LOCKED)
            else:
                self.change_current_room(self.player_room.exits[direction])
                print(self.get_description())
        else:
            print(NO_EXIT)

    def get_item_by_id(self,item_id):
        for item in self.items_repository:
            if item.id == item_id:
                return item
        return False

    def get_description(self):
        retstr = self.player_room.description+"\n"
        for i in self.player_room.items:
            retstr += self.get_item_by_id(i).description+"\n"
        for d,r in self.player_room.exits.items():
            direction = ""
            if d is 'n':
                direction = NORTH_NAME
            elif d is 'w':
                direction = WEST_NAME
            elif d is 's':
                direction = SOUTH_NAME
            elif d is 'e':
                direction = EAST_NAME
            elif d is 'u':
                direction = UP_NAME.lower()
            elif d is 'd':
                direction = DOWN_NAME.lower()
            room_name = self.get_room_by_id(r).name.lower()
            if d in self.player_room.locked.keys():
                retstr += self.player_room.locked[d][0] % direction
            else:
                retstr += SEE_DOOR % (room_name, direction) # "You can see doors leading to the "+room_name+" to the "+direction+".\n"
            retstr += "\n"
        return retstr
                 
    def get_item_by_name(self,item_name):
        for i in self.items_repository:
            #item = self.get_item_by_id(i)
            if item_name.upper().lower() in i.names:#i.name.upper().lower() == item_name.upper().lower():
                return i
        return False

    def take(self, item_name):
        if len(self.player_room.items) == 0:
            print(CANNOT_TAKE)
            return
        item = [item for item in self.items_repository if item_name in item.names and item.id in self.player_room.items][0]
        #item = self.get_item_by_name(item_name)
        if not item:
            print(NO_SUCH_ITEM)
        if item.id in self.player_room.items:
            self.inventory.append(item.id)
            self.player_room.items.remove(item.id)
            print(TAKE_ITEM % item.name)
        else:
            print(CANNOT_TAKE)

    def pick(self,item):
        if item in self.player_room.items:
            self.inventory.append(item)
            self.player_room.items.remove(item)
        else:
            print(CANNOT_TAKE)
    
    def inspect(self):
        print(self.get_description())

    def sorry(self):
        print(SORRY_STRING)
    
    def look_at(self,item_name):
        if item_name.upper().lower() == "inventory":
            if len(self.inventory) == 0:
                print(EMPTY_INVENTORY)
                return
            all_items = INVENTORY_DESCRIPTION
            for i in self.inventory:
                it = self.get_item_by_id(i)
                all_items += "\n"
                all_items += it.description_inventory
            print(all_items)
            return
        item = self.get_item_by_name(item_name)
        if item:
            if item.id in self.player_room.items:
                print(item.description)
            elif item.id in self.inventory:
                print(item.description_inventory)
        else:
            print(CANNOT_LOOK)

    def open(self,item):
        if item in self.player_room.items:
            item.call('open')
        elif item in self.inventory:
            item.call('open')

    def close(self,item):
        if item in self.player_room.items:
            item.call('close')
        elif item in self.inventory:
            item.call('close')

    def read(self,item):
        if item in self.player_room.items:
            item.call('read')
        elif item in self.inventory:
            item.call('read')

    def push(self,item):
        if item in self.player_room.items:
            item.call('push')
        elif item in self.inventory:
            item.call('push')

    def pull(self,item):
        if item in self.player_room.items:
            item.call('pull')
        elif item in self.inventory:
            item.call('pull')

    def eat(self,item_name):
        item = self.get_item_by_name(item_name)
        if item.id in self.player_room.items and item.attributes['consumable']:
            self.player_room.items.remove(item.id)
            exec(item.attributes['consumable_code'])
        elif item.id in self.inventory and item.attributes['consumable']:
            self.inventory.remove(item.id)
            self.execute(item.attributes['consumable_code'])
        else:
            print(CANNOT_EAT)

    def talk(self,receiver):
        #talk to person in room or inventory
        pass

    def give(self,item):
        #give item from inventory to person in current room
        pass

    def use(self,item1,item2):
        #use item on second item
        #pass
        if (item1 in self.inventory) and (item2 in self.inventory or item2 in self.player_room.items):
            item1.combine(item2)
        else:
            print(CANNOT_USE)

    def put(self,item):
        #talk to item in room or inventory
        pass

    def unlock(self,direction):
        #can be direction
        keys = []
        for i in self.inventory:
            item = self.get_item_by_id(i)
            if item.attributes['key']:
                keys.append(item)
        if len(keys) == 0:
            print(HAVE_NO_KEYS)
            return
        keyhashes = []
        for k in keys:
            keyhashes.append(k.attributes["keyhash"])
        if direction in NORTH_STRINGS:
            direction = NORTH_ABBREV
        if direction in WEST_STRINGS:
            direction = WEST_ABBREV
        if direction in SOUTH_STRINGS:
            direction = SOUTH_ABBREV
        if direction in EAST_STRINGS:
            direction = EAST_ABBREV
        if direction in UP_STRINGS:
            direction = UP_ABBREV
        if direction in DOWN_STRINGS:
            direction = DOWN_ABBREV
        if direction not in self.player_room.locked.keys():
            print(ALREADY_UNLOCKED)
        else:
            if self.player_room.locked[direction][2] in keyhashes:
                right_key = [key for key in keys if key.attributes["keyhash"]==self.player_room.locked[direction][2]][0]
                print(self.player_room.locked[direction][1])
                del self.player_room.locked[direction]
                #self.player_room.locked.remove(direction)
                #self.inventory.pop(right_key.id)
                #del self.inventory[right_key.id]
                self.inventory.remove(right_key.id)
            else:
                print(WRONG_KEY)
        

class Item:
    def __init__(self,item_data,gs=None):
        self.game_state = gs
        self.id = item_data['id']
        self.name = item_data['name']
        self.names = item_data['names']
        self.description = item_data['description']
        self.inspect = item_data['inspect']
        self.description_inventory = item_data['description_inventory']
        self.attributes = item_data['attributes']
    
    def combine(self,second_item):
        #combine the two items
        #pass
        pass

    def call(self,activity):
        getattr(self,activity,game_state.sorry)()


class Parser:
    def __init__(self,gs):
        self.game_state = gs

    def parse_movement(self,direction):
        if direction in NORTH_STRINGS:
            self.game_state.move('n')
        elif direction in WEST_STRINGS:
            self.game_state.move('w')
        elif direction in SOUTH_STRINGS:
            self.game_state.move('s')
        elif direction in EAST_STRINGS:
            self.game_state.move('e')
        elif direction in UP_STRINGS:
            self.game_state.move('u')
        elif direction in DOWN_STRINGS:
            self.game_state.move('d')
        
    def parse(self,inp):
        inp = inp.upper().lower()
        if inp == " " or inp == "":
            print(SORRY_STRING)
            return
        inp_split = inp.split()
        #if len(inp_split) == 1:
        if inp_split[0] == 'look':
            if len(inp_split) > 1:
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
        elif inp_split[0] in UP_STRINGS:
            self.game_state.move('u')
        elif inp_split[0] in DOWN_STRINGS:
            self.game_state.move('d')
        elif inp_split[0] in MOVE_VERBS:
            #self.parse(inp_split[1:])
            #self.game_state.move(inp_split[1])
            self.parse_movement(inp_split[1])
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
        elif inp_split[0] == 'eat':
            self.game_state.eat(inp_split[-1])
        elif inp_split[0] == 'unlock':
            self.game_state.unlock(inp_split[-1])
        #these need more
        elif inp_split[0] == 'give':
            self.game_state.give(inp_split[1],inp_split[3])
        elif inp_split[0] == 'use':
            self.game_state.give(inp_split[1],inp_split[3])
        elif inp_split[0] == 'put':
            self.game_state.give(inp_split[1],inp_split[3])
        elif inp=='use key on door':
            self.game_state.unlock()
        else:
            self.game_state.sorry()
        
        
class Room:
    def __init__(self, room_data,gs=None):
        self.id = room_data['ID']
        self.name = room_data['name']
        self.description = room_data['description']
        self.exits = room_data['exits']
        self.game_state = gs
        self.special = room_data['special']
        self.items = room_data['items']
        self.locked = room_data['locked']




game_state = GameState()
print("Welcome to Zork!")
print(game_state.get_description())
while(game_state.loop):
    print()
    #print(game_state.get_description())
    inp = input("Order:")#input("What would you like to do next?\n")
    game_state.parser.parse(inp)
    #game_state.player_room.exit(inp)
