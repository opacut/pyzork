import json

FILE_PATH = 'rooms.json'

class GameState:
    def __init__(self):
        self.rooms = self.get_rooms_from_file(FILE_PATH)
        self.current_room = None
        self.change_current_room('Entrance')
        self.loop = True

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



class Room:
    def __init__(self, room_data):
        self.name = room_data['name']
        self.description = room_data['description']
        self.exits = room_data['exits']
    
    def exit(self, direction):
        global game_state
        if direction not in exit_codes.keys():
            if direction == "sleep":
                self.sleep()
            else:
                "Invalid input."
        elif self.exits[exit_codes[direction]] == "none":
            print("There is nothing there!")
        else:
            game_state.change_current_room(self.exits[exit_codes[direction]])

    def sleep(self):
        global game_state
        if(self.name=="bedroom"):
            print("Good night!")
            game_state.quit_game()
        else:
            print("You can't sleep here!")

def parse(self,inp):
    def move_to(i):
        if inp=='n' or inp=='north' or inp=='notrh':
            # go North
            pass
        elif inp=='w' or inp=='west' or inp=='wset':
            #go West
            pass
        elif inp=='s' or inp=='south' or inp=='sotuh':
            # go South
            pass
        elif inp=='e' or inp=='east' or inp=='esat':
            #go East
            pass
        else:
            sorry()
    def sorry():
        print('I\'m sorry, I didn\'t catch that.')

    inp = inp.upper().lower()
    inp_split = inp.split()
    if len(inp_split) == 1:
        if inp_split[0] == 'look' or inp_split[0] == 'inspect':
            # look around
            pass
        elif inp_split[0] in ['n','w','s','e','north','west','south','east']:
            move_to(inp_split[0])
        else:
            sorry()
    if inp_split[0] == 'go':
        move_to(inp_split[1])
    elif inp_split[0] == 'take':
        #take inp_split[-1]
        pass
    elif inp_split[0] == 'look':
        #look at inp_split[-1]
        pass
    elif inp_split[0] == 'open':
        #open inp_split[-1]
        pass
    elif inp_split[0] == 'close':
        #close inp_split[-1]
        pass
    elif inp_split[0] == 'push':
        #push inp_split[-1]
        pass
    elif inp_split[0] == 'pull':
        #pull inp_split[-1]
        pass
    elif inp_split[0] == 'pick':
        #pick up inp_split[-1]
        pass
    elif inp_split[0] == 'talk':
        #talk to inp_split[-1]
        pass
    elif inp_split[0] == 'give':
        #give inp_split[1] to inp_split[3]
        pass
    elif inp_split[0] == 'use':
        #use inp_split[1] on inp_split[3]
        pass
    elif inp_split[0] == 'put':
        #put inp_split[1] into inp_split[3]
        pass
    else:
        sorry()
        



exit_codes = {
    "n":0,
    "w":1,
    "s":2,
    "e":3
}


game_state = GameState()
print("Welcome to Zork!")
while(game_state.loop):
    print()
    print(game_state.current_room.description)
    inp = input("What would you like to do next?\n")

    game_state.current_room.exit(inp)
