from .app import Room, EXIT_CODES, GameState

class Entrance(Room):
    def __init__(self, room_data,gs=None):
        Room.__init__(self,room_data,gs)
    #    self.name = room_data['name']
    #    self.description = room_data['description']
    #    self.exits = room_data['exits']
    #    self.game_state = gs
    #    self.special = room_data['special']
    #    self.items = room_data['items']
    
    #def exit(self, direction):
    #    global game_state
    #    if direction not in EXIT_CODES.keys():
    #        if direction == "sleep":
    #            self.sleep()
    #        else:
    #            "Invalid input."
    #    elif self.exits[EXIT_CODES[direction]] == "none":
    #        print("There is nothing there!")
    #    else:
    #        self.game_state.change_current_room(self.exits[EXIT_CODES[direction]])