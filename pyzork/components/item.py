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
        pass

    def call(self,activity):
        #getattr(self,activity,game_state.sorry)()
        pass