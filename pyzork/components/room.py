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
        self.additional_description = room_data['additional_description']
