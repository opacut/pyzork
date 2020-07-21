from components.game_state import GameState



def run():
    game_state = GameState()
    print("Welcome to Zork!")
    print(game_state.get_description())
    while(game_state.loop):
        print()
        #print(game_state.get_description())
        inp = input("Order:")#input("What would you like to do next?\n")
        game_state.parser.parse(inp)
        #game_state.player_room.exit(inp)
