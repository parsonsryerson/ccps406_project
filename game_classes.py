class WorldObject():

    # Constructor
    def __init__(self, name:str, state:dict, starting_state:str) -> None:
        self._name = name
        self._state = state
        self._current_state = starting_state
        self._description_length = 'long'

    # Setter Methods
    def set_current_state(self, next_state:str) -> None:
        self._current_state = next_state
        self._description_length = 'long'

    # Getter Methods
    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        result = self._state.get(self._current_state).get('description').get(self._description_length)
        # Set description length to 'short' when 'long' description is requested
        if self._description_length == 'long':
            self._description_length = 'short'
        return result

    def get_current_state(self) -> str:
        return self._current_state

    def get_is_player(self) -> bool:
        # to be overriden by subclasses
        return False




class Room(WorldObject):

    # Constructor
    def __init__(self, name:str, state:dict, starting_state:str) -> None:
        super().__init__(name, state, starting_state)
        # override
        self._connections = self._state.get(self._current_state).get('connections')
        self._game_objects = {}

    # Setter Methods

    # override
    def set_current_state(self, next_state:str) -> None:
        self._current_state = next_state
        self._description_length = 'long'
        self.set_connections(self._state.get(self._current_state).get('connections'))

    def set_connections(self, connections:dict) -> None:
        self._connections.update(connections)

    def set_game_objects(self, game_objects:dict) -> None:
        self._game_objects.update(game_objects)

    def remove_game_objects(self, game_object_key:str) -> None:
        self._game_objects.pop(game_object_key)

    # Getter Methods
    def get_room_name(self) -> str:
        return self._name

    def get_connections(self) -> dict:
        return self._connections

    def get_game_objects(self) -> dict:
        return self._game_objects





class GameObject(WorldObject):

    # Constructor
    def __init__(self, name:str, state:dict, starting_room_name:str, starting_state:str) -> None:
        super().__init__(name, state, starting_state)
        self._current_room_name = starting_room_name

    # Setter Method
    def set_room_name(self,room_name) -> None:
        self._current_room_name = room_name

    # Getter Method
    def get_room_name(self) -> str:
        return self._current_room_name





class Character(GameObject):

    # Constructor
    def __init__(self, name:str, state:dict, starting_room_name:str, starting_state:str, is_player:bool) -> None:
        super().__init__(name, state, starting_room_name, starting_state)
        self._inventory = {}
        self._is_player = is_player

    # Returns dict of Items currently held
    def get_inventory(self) -> dict:
        return self._inventory

    # Adds Item to inventory
    def add_to_inventory(self, items_to_add) -> None:
        self._inventory.update(items_to_add)

    # Removes Item from inventory
    def remove_from_inventory(self, items_to_remove) -> None:
        for item_name,item in items_to_remove.items():
            self._inventory.pop(item_name,'')

    # Override WorldObject method
    def get_is_player(self) -> bool:
        return self._is_player





class Item(GameObject):

    # Constructor
    def __init__(self, name:str, state:dict, starting_room_name:str, starting_state:str, is_carryable:bool, is_equippable:bool) -> None:
        super().__init__(name, state, starting_room_name, starting_state)
        self._in_inventory_of = None
        self._is_carryable = is_carryable
        self._is_equippable = is_equippable

    # Returns the Character for which the Item is currently in the inventory of, otherwise None
    def get_inventory_of(self):
        return self._in_inventory_of

    # Adds the Character as the holder of the Item
    def add_inventory_of(self,character_name) -> None:
        self._in_inventory_of = character_name

    # Removes the Character as the holder of the Item
    def remove_inventory_of(self) -> None:
        self._in_inventory_of = None





class Action():

    # Constructor
    def __init__(self, available_actions:dict = {}, action_name:str = '', actor_name:str = '', target_name:str = '') -> None:
        self._action_name = action_name
        self._actor_name = actor_name
        self._target_name = target_name
        self._req_state = {}
        self._next_state = {}
        self._description_success = ''

        if action_name in available_actions.keys():
            # get specific action/target details from available actions
            action_dict = available_actions.get(self._action_name)
            target_dict = action_dict.get(self._target_name)

            # if specific action/target details exist, extract the required and next state information
            if target_name in action_dict.keys() and action_name != 'describe':
                self._req_state = target_dict.get('req_state')
                self._next_state = target_dict.get('next_state')
                self._description_success = target_dict.get('description_success')
        print(f"DEBUG - action_name: {action_name}, actor_name: {actor_name}, target_name: {target_name}, req_state: {self._req_state}, next_state: {self._next_state}, description: {self._description_success}")


    # Setter Functions
    def set_target_name(self, target_name) -> None:
        self._target_name = target_name

    # Getter Functions
    def get_actor_name(self) -> str:
        return self._actor_name

    def get_target_name(self) -> str:
        return self._target_name

    def get_action_name(self) -> str:
        return self._action_name

    def get_req_state(self):
        return self._req_state

    def get_next_state(self):
        return self._next_state

    def get_description_success(self):
        return self._description_success