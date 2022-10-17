import json
from constants import ConstantsProvider as cte
from parser import Parser
from components.room import Room
from components.item import Item
from random import choice

class GameState:
    def __init__(self, monster=True):
        self.rooms = self.get_rooms_from_file(cte.FILE_PATH)
        self.item_attribute_pairs = self.get_item_attributes_from_file(cte.ITEM_ATTRS_FILE_PATH)
        self.items_repository = self.get_items_from_file(cte.ITEM_FILE_PATH)
        self.player_room = None
        self.change_current_room(cte.STARTING_ROOM_PLAYER)
        self.loop = True
        self.parser = Parser(self)
        self.inventory = list()
        self.monster = monster
        if monster:
            self.monster_room = cte.STARTING_ROOM_MONSTER
            self.move_monster(cte.STARTING_ROOM_MONSTER,init=True)
            #self.close_rooms = list(self.get_room_by_id(self.monster_room).exits.values())
            #self.far_rooms = 
            #print(self.close_rooms)
        #self.room_index = self.build_rooms_index

    # returns a dictionary with room id as key and where the sound is coming from as value  ###returns a list of tuples, where first element is direction from which the sound is comind and second is the room id   ###returns a dictionary where the key is where the sound is coming from and the value is the room id
    def get_close_rooms(self,room_id):
        room = self.get_room_by_id(room_id)
        #close_room_tuples = []
        close_room_dict = {}
        for ex, i in room.exits.items():
            if ex == 'n':
                #tup = ('s',ex)
                #close_room_tuples.append(tup)
                close_room_dict[i] = 's'
            elif ex == 'w':
                #tup = ('e',ex)
                #close_room_tuples.append(tup)
                close_room_dict[i] = 'e'
            elif ex == 's':
                #tup = ('n',ex)
                #close_room_tuples.append(tup)
                close_room_dict[i] = 'n'
            elif ex == 'e':
                #tup = ('w',ex)
                #close_room_tuples.append(tup)
                close_room_dict[i] = 'w'
            elif ex == 'u':
                #tup = ('d',ex)
                #close_room_tuples.append(tup)
                close_room_dict[i] = 'd'
            elif ex == 'd':
                #tup = ('u',ex)
                #close_room_tuples.append(tup)
                close_room_dict[i] = 'u'
        return close_room_dict#close_room_dict #list(self.get_room_by_id(self.monster_room).exits.values())

    def get_far_rooms(self,room_id):
        far_rooms = {}
        close_rooms = list(self.get_close_rooms(room_id).keys())
        for r in close_rooms:#list(self.get_close_rooms(room_id).keys()):
            room = self.get_room_by_id(r)
            ks = list(room.exits.keys())
            for ex, i in room.exits.items():
                if i == room_id or i in close_rooms:
                    pass
                elif ex == 'n':
                    if i in ks:  
                        far_rooms[i] += 's'
                    else:
                        far_rooms[i] = 's'
                elif ex == 'w':
                    if i in ks:
                        far_rooms[i] += 'e'
                    else: 
                       far_rooms[i] = 'e'
                elif ex == 's':
                    if i in ks:
                        far_rooms[i] += 'n'
                    else:
                        far_rooms[i] = 'n'
                elif ex == 'e':
                    if i in ks:
                        far_rooms[i] += 'w'
                    else:
                        far_rooms[i] = 'w'
                elif ex == 'u':
                    if i in ks:
                        far_rooms[i] += 'd'
                    else:
                        far_rooms[i] = 'd'
                elif ex == 'd':
                    if i in ks:
                        far_rooms[i] += 'u'
                    else:
                        far_rooms[i] = 'u'

        return far_rooms
                #if j.id not in done:
                #    done.append(j.id)
                #pass
        #return far_room_tuples

    def monster_location(self):
        print("Monster is in "+str(self.monster_room)+".")

    def move_monster(self,room_id,init=False):
        #remove old
        if not init:
            for r in self.get_close_rooms(self.monster_room):
                del self.get_room_by_id(r).additional_description['monster_close']
            for r in self.get_far_rooms(self.monster_room):
                del self.get_room_by_id(r).additional_description['monster_far']
        #add new
        if room_id == self.player_room.id:
            print("You have been eaten, GAME OVER!")
            print("DEBUG: PLAYER: "+str(self.player_room.id)+" MONSTER: "+str(self.monster_room))
            self.quit_game()
            return
        self.monster_room = room_id
        close_rooms = self.get_close_rooms(self.monster_room)
        #far_rooms = self.get_far_rooms(self.monster_room)
        for r,d in close_rooms.items():
            room = self.get_room_by_id(r)
            room.additional_description['monster_close'] = "Monster is close. You hear loud stomps to the "+d
        far_rooms = self.get_far_rooms(self.monster_room)
        for r,d in far_rooms.items():
            room = self.get_room_by_id(r)
            room.additional_description['monster_far'] = "Monster is somewhere around. You hear quiet rustling to the "+d.split()[0]
            for s in d.split():
                if s == d.split()[0]:
                    pass
                else:
                    room.additional_description['monster_far'] += "and "+s
            #room.additional_description['monster_far'] += ".\n"
            #r.additional_description += "Monster is close."

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

    def get_random_room_id_for_monster(self):
        mr = self.get_room_by_id(self.monster_room)
        exs = list(mr.exits.values())
        for i in mr.locked:
            if i in exs:
                exs.remove(i)
        return choice(exs)
        

    def move(self,direction):
        #index = EXIT_CODES[direction]
        if direction in self.player_room.exits.keys():
            if direction in self.player_room.locked:
                print(cte.LOCKED)
            else:
                monster_room_new = self.get_random_room_id_for_monster()
                #if self.player_room.exits[direction] == monster_room_new:
                if self.player_room.id == monster_room_new and self.player_room.exits[direction] == self.monster_room:
                    print("You have been eaten, GAME OVER!")
                    print("DEBUG: PLAYER: "+str(self.player_room.id)+" to "+str(self.player_room.exits[direction])+" MONSTER: "+str(self.monster_room)+" to "+str(monster_room_new))
                    self.quit_game()
                    return
                self.change_current_room(self.player_room.exits[direction])
                if self.monster:
                    if self.monster_room == self.player_room:
                        print("You have been eaten, GAME OVER!")
                        self.quit_game()
                        return
                    else:
                        self.move_monster(monster_room_new)
                print(self.get_description())
        else:
            print(cte.NO_EXIT)

    def get_item_by_id(self,item_id):
        for item in self.items_repository:
            if item.id == item_id:
                return item
        return False

    def get_description(self):
        retstr = self.player_room.description+"\n"
        for i in self.player_room.additional_description.values():
            retstr += i+"\n"
        for i in self.player_room.items:
            retstr += self.get_item_by_id(i).description+"\n"
        for d,r in self.player_room.exits.items():
            direction = ""
            if d == 'n':
                direction = cte.NORTH_NAME
            elif d == 'w':
                direction = cte.WEST_NAME
            elif d == 's':
                direction = cte.SOUTH_NAME
            elif d == 'e':
                direction = cte.EAST_NAME
            elif d == 'u':
                direction = cte.UP_NAME.lower()
            elif d == 'd':
                direction = cte.DOWN_NAME.lower()
            room_name = self.get_room_by_id(r).name.lower()
            if d in self.player_room.locked.keys():
                retstr += self.player_room.locked[d][0] % direction
            else:
                retstr += cte.SEE_DOOR % (room_name, direction) # "You can see doors leading to the "+room_name+" to the "+direction+".\n"
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
            print(cte.CANNOT_TAKE)
            return
        item = [item for item in self.items_repository if item_name in item.names and item.id in self.player_room.items][0]
        #item = self.get_item_by_name(item_name)
        if not item:
            print(cte.NO_SUCH_ITEM)
        if item.id in self.player_room.items:
            self.inventory.append(item.id)
            self.player_room.items.remove(item.id)
            print(cte.TAKE_ITEM % item.name)
        else:
            print(cte.CANNOT_TAKE)

    def pick(self,item):
        if item in self.player_room.items:
            self.inventory.append(item)
            self.player_room.items.remove(item)
        else:
            print(cte.CANNOT_TAKE)
    
    def inspect(self):
        print(self.get_description())

    def sorry(self):
        print(cte.SORRY_STRING)
    
    def look_at(self,item_name):
        if item_name.upper().lower() == "inventory":
            if len(self.inventory) == 0:
                print(cte.EMPTY_INVENTORY)
                return
            all_items = cte.INVENTORY_DESCRIPTION
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
            print(cte.CANNOT_LOOK)

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
            #self.inventory.remove(item.id)
            self.execute(item.attributes['consumable_code'])
        else:
            print(cte.CANNOT_EAT)

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
            print(cte.CANNOT_USE)

    def cut(self,item1,item2):
        item_one = self.get_item_by_name(item1)
        if not item_one or item_one.id not in self.inventory:
            print(cte.NO_SUCH_ITEM)
            return
        item_two = self.get_item_by_name(item2)
        if not item_two or item_two.id not in self.inventory:
            print(cte.NO_SUCH_ITEM)
            return
        if not item_two.attributes['cutter']:
            print(cte.NOT_A_CUTTER)
            return
        if not item_one.attributes['cuttable']:
            print(cte.NOT_CUTTABLE)
            return
        self.execute(item_one.attributes['cuttable_code'])

    def wait(self):
    
        if self.monster:
            self.move_monster(self.get_random_room_id_for_monster())
            if self.monster_room == self.player_room:
                print("You have been eaten, GAME OVER!")
                self.quit_game()
                return
            else:
                print(self.get_description())
        else:
            print("Time passes")
            print(self.get_description())

    def put(self,item):
        #talk to item in room or inventory
        pass

    def unlock(self,direction):
        #can be direction
        if "door" in direction:
            print("You need to specify a direction to unlock!")
            return
        keys = []
        for i in self.inventory:
            item = self.get_item_by_id(i)
            if item.attributes['key']:
                keys.append(item)
        if len(keys) == 0:
            print(cte.HAVE_NO_KEYS)
            return
        keyhashes = []
        for k in keys:
            keyhashes.append(k.attributes["keyhash"])
        if direction in cte.NORTH_STRINGS:
            direction = cte.NORTH_ABBREV
        if direction in cte.WEST_STRINGS:
            direction = cte.WEST_ABBREV
        if direction in cte.SOUTH_STRINGS:
            direction = cte.SOUTH_ABBREV
        if direction in cte.EAST_STRINGS:
            direction = cte.EAST_ABBREV
        if direction in cte.UP_STRINGS:
            direction = cte.UP_ABBREV
        if direction in cte.DOWN_STRINGS:
            direction = cte.DOWN_ABBREV
        if direction not in self.player_room.locked.keys():
            print(cte.ALREADY_UNLOCKED)
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
                print(cte.WRONG_KEY)