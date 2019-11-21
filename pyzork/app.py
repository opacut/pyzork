print("Welcome to Zork!")

def change_current_room(room):
    global current_room 
    current_room = rooms[room]

class Room:
    def __init__(self, name="", description="", exits=list()):
        self.name = name
        self.description = description
        self.exits = exits
    
    def exit(self, direction):
        if direction not in exit_codes.keys():
            if direction == "sleep":
                self.sleep()
            else:
                "Invalid input."
        elif self.exits[exit_codes[direction]] == "none":
            print("There is nothing there!")
        else:
            change_current_room(self.exits[exit_codes[direction]])

    def sleep(self):
        if(self.name=="bedroom"):
            print("Good night!")
            global loop
            loop = not loop
        else:
            print("You can't sleep here!")


#class Item:

exit_codes = {
    "n":0,
    "w":1,
    "s":2,
    "e":3
}

rooms = {
    "entrance": Room("entrance", "Welcome. Go n/s/e.", ["dining", "none", "kitchen", "living"]),
    "dining": Room("dining","Dining room! Go n/s.", ["patio", "none", "entrance", "none"]),
    "patio": Room("patio", "Welcome to the patio. Go s/e.", ["none","none","dining","tower"]),
    "kitchen": Room("kitcher", "cooking time in the kitchen! Go n/e.", ["entrance","none","none","bedroom"]),
    "tower": Room("tower", "Tower up! Go w/s.",["none","patio","living","none"]),
    "living": Room("living","Living room! Go n/w/e.",["tower","entrance","none","taxidermy"]),
    "taxidermy": Room("taxidermy","Taxidermy room. Go w/s.",["none","living","bedroom","none"]),
    "bedroom": Room("bedroom","Bedroom. Good night! Go n/w",["taxidermy","kitchen","none","none"])
}

current_room = Room()
loop = True
change_current_room("entrance")
while(loop):
    print()
    print(current_room.description)
    inp = input("What would you like to do next?\n")
    current_room.exit(inp)
