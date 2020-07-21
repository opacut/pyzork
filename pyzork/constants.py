class ConstantsProvider:
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
    STARTING_ROOM_MONSTER = 5 #"bedroom"
    NO_EXIT = "There is no passage that way."
    SEE_DOOR = "You can see doors leading to the %s to the %s."
    INVENTORY_DESCRIPTION = "You are carrying: "
    EMPTY_INVENTORY = "Your inventory is empty."
    HAVE_NO_KEYS = "You don't have any keys!"
    ALREADY_UNLOCKED = "That direction is already accessible!"
    NO_SUCH_ITEM = "There is no such item in here."
    WRONG_KEY = "The key doesn't fit!"
    NOT_CUTTABLE = "You can't cut that!"
    NOT_A_CUTTER = "That won't cut anything!"
    EXIT_CODES = {
        'n':0,
        'w':1,
        's':2,
        'e':3,
        'u':4,
        'd':5
    }

    def constant(self, name):
        return getattr(self, name)