from constants import ConstantsProvider as cte

class Parser:
    def __init__(self,gs):
        self.game_state = gs

    def _parse_movement(self,direction):
        if direction in cte.NORTH_STRINGS:
            self.game_state.move('n')
        elif direction in cte.WEST_STRINGS:
            self.game_state.move('w')
        elif direction in cte.SOUTH_STRINGS:
            self.game_state.move('s')
        elif direction in cte.EAST_STRINGS:
            self.game_state.move('e')
        elif direction in cte.UP_STRINGS:
            self.game_state.move('u')
        elif direction in cte.DOWN_STRINGS:
            self.game_state.move('d')

    def _sorry(self):
        print(cte.SORRY_STRING)
        
    def parse(self,inp):
        inp = inp.upper().lower()
        if inp == " " or inp == "":
            self._sorry()
            return
        inp_split = inp.split()
        #if len(inp_split) == 1:
        if inp_split[0] == 'wait':
            self.game_state.wait()
        elif inp_split[0] == 'look':
            if len(inp_split) > 1:
                if inp_split[1]=='around':
                    self.game_state.inspect()
                else:
                    self.game_state.look_at(inp_split[-1])
        elif inp_split[0] in cte.NORTH_STRINGS:
            self.game_state.move('n')
        elif inp_split[0] in cte.WEST_STRINGS:
            self.game_state.move('w')
        elif inp_split[0] in cte.SOUTH_STRINGS:
            self.game_state.move('s')
        elif inp_split[0] in cte.EAST_STRINGS:
            self.game_state.move('e')
        elif inp_split[0] in cte.UP_STRINGS:
            self.game_state.move('u')
        elif inp_split[0] in cte.DOWN_STRINGS:
            self.game_state.move('d')
        elif inp_split[0] in cte.MOVE_VERBS:
            #self.parse(inp_split[1:])
            #self.game_state.move(inp_split[1])
            self._parse_movement(inp_split[1])
        elif inp_split[0] == 'take' and len(inp_split)>1:
            self.game_state.take(inp_split[-1])
        elif inp_split[0] == 'open' and len(inp_split)>1:
            self.game_state.open(inp_split[-1])
        elif inp_split[0] == 'close' and len(inp_split)>1:
            self.game_state.close(inp_split[-1])
        elif inp_split[0] == 'read' and len(inp_split)>1:
            self.game_state.read(inp_split[-1])
        elif inp_split[0] == 'push' and len(inp_split)>1:
            self.game_state.push(inp_split[-1])
        elif inp_split[0] == 'pull' and len(inp_split)>1:
            self.game_state.pull(inp_split[-1])
        elif inp_split[0] == 'pick' and len(inp_split)>1:
            self.game_state.pick(inp_split[-1])
        elif inp_split[0] == 'talk' and len(inp_split)>1:
            self.game_state.talk(inp_split[-1])
        elif inp_split[0] == 'eat' and len(inp_split)>1:
            self.game_state.eat(inp_split[-1])
        elif inp_split[0] == 'unlock' and len(inp_split)>1:
            self.game_state.unlock(inp_split[-1])
        #these need more
        elif inp_split[0] == 'give' and len(inp_split)>3:
            self.game_state.give(inp_split[1],inp_split[-1])
        elif inp_split[0] == 'use' and len(inp_split)>3:
            self.game_state.use(inp_split[1],inp_split[-1])
        elif inp_split[0] == 'put' and len(inp_split)>3:
            self.game_state.put(inp_split[1],inp_split[-1])
        elif inp_split[0] == 'cut' and len(inp_split)>3:
            self.game_state.cut(inp_split[1],inp_split[-1])
        elif inp=='use key on door':
            self.game_state.unlock()
        elif inp=='ml':
            self.game_state.monster_location()
        elif inp=="quit":
            self.game_state.quit_game()
        elif inp=="inventory":
            self.game_state.look_at("inventory")
        else:
            self.game_state.sorry()