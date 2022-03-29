class CommandParser():

    # Constructor
    def __init__(self, input_string:str = '') -> None:
        self._input_string = input_string
        self._action = None
        self._actor = None
        self._target = None

    # Translates input string into three key aspects
    # - Actor - the object performing the action
    # - Action - the action being performed
    # - Target - the object the action is being performed on
    def parse_command(self, command: str) -> None:
        ## parse the command
        # tbd
        # action = ...
        # actor = ...
        # target = ...
        # self.__set_action(action)
        # self.__set_actor(actor)
        # self.__set_target(target)
        pass

    # Setter Methods (private)
    def __set_action(self, action: str) -> None:
        self._action = action

    def __set_actor(self, actor) -> None:
        self._actor = actor

    def __set_target(self, target) -> None:
        self._target = target

    # Getter Methods (public)
    def get_action(self) -> str:
        return self._action

    def get_actor(self):
        return self._actor

    def get_target(self):
        return self._target





class World():

    # Constructor
    def __init__(self, world_objects:dict = {}, available_actions:dict = {}) -> None:
        self._world_objects = world_objects
        self._available_actions = available_actions
        self._is_game_over = False
        self._player_name = find_player_name(world_objects)

    # make player name directly available from world class for convenience
    def find_player_name(self,world_objects:dict) -> str:
        for obj_name,obj_value in world_objects.items():
            if obj_value.get_is_player():
                return obj_name
        return ''

    # Setter Methods
    def set_world_objects(self, world_objects: dict) -> None:
        self._world_objects.update(world_objects)

    def set_available_actions(self, available_actions:dict) -> None:
        self._available_actions.update(available_actions)
    
    def set_game_over(self, game_over: bool) -> None:
        self._is_game_over = game_over
    
    # Getter Methods
    def get_world_objects(self) -> dict:
        return self._world_objects

    def get_available_actions(self) -> dict:
        return self._available_actions

    def get_player_name(self) -> str:
        return self._player_name

    def is_game_over(self) -> bool:
        return self._is_game_over






class WorldObject():

    # Constructor
    def __init__(self, name:str, state:dict) -> None:
        self._name = name
        self._state = state
        self._current_state = 'init'
        self._description_length = 'long'

    # Setter Methods
    def set_current_state(self, next_state:str) -> None:
        self._current_state = next_state
        # Reset description length to 'long' when WorldObject changes state
        self._description_length = 'long'

    # Getter Methods
    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        result = _state.get(self._current_state,'').get('description','').get(_description_length,'')
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
    def __init__(self, name:str, state:dict) -> None:
        super().__init__(name,state)
        self._connections = {}
        self._game_objects = {}

    # Setter Methods
    def set_connections(self, connections:dict) -> None:
        self._connections.update(connections)

    def set_game_objects(self, game_objects:dict) -> None:
        self._game_objects.update(game_objects)

    # Getter Methods
    def get_connections(self) -> dict:
        return self._connections

    def get_game_objects(self) -> dict:
        return self._game_objects






class GameObject(WorldObject):

    # Constructor
    def __init__(self, name:str, state:dict, starting_room_name:str) -> None:
        super().__init__(name,state)
        self._current_room_name = starting_room_name

    # # Performs the action by the actor on the target
    # def perform_action(action:str, world) -> None:
    #     # tbd
    #     # if 'action' is performed: 
    #     # check data for what the state transition looks like for
    #     # both the game object and the target 
    #     # should be list of "available actions" for each object in each state
    #     # it should contain the next state name for both actor and target
    #     pass

    # Setter Method
    def set_room_name(self,room_name) -> None:
        self.current_room_name = room_name

    # Getter Method
    def get_room_name(self) -> str:
        return self._current_room_name





class Character(GameObject):

    # Constructor
    def __init__(self, name:str, state:dict, starting_room_name:str, is_player:bool) -> None:
        super().__init__(name,state,starting_room_name)
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
    def __init__(self, name:str, state:dict, starting_room_name:str, is_carryable:bool, is_equippable:bool) -> None:
        super().__init__(name,state,starting_room_name)
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
    def __init__(self, name:str, actor_name:str, target_name:str, req_state:dict, next_state:dict, description_success:str) -> None:
        self._name = name
        self._actor_name = actor_name
        self._target_name = target_name
        self._req_state = req_state
        self._next_state = next_state
        self._description_success = description_success

    def perform_action(self, world) -> str:
        # initialize result to empty string
        result = ''

        # special case - "describe" action always meets conditions
        if self._name == "describe":
            result = self.perform_describe(world)

        # general case - check if conditions for actions are met, if so update states and return success description
        if self.meets_conditions(world):
            self.update_states(world)
            result = self._description_success
        return result

    def perform_describe(self, world) -> str:
        # if no target specified, assume target is current room of player
        if self._target_name is None:
            actor = world.get_world_objects().get(world.get_player_name(),None)
            target = world.get_world_objects().get(actor.get_room_name(),None)
        else:
            target = world.get_world_objects().get(self._target_name,None)
        return target.get_description()

    def update_states(self, world) -> None:
        for name, next_state in self._next_state.items(): 
            world_object = world.get_world_objects().get(name,None)
            if world_object is not None:
                world_object.set_current_state(next_state)

    def meets_conditions(self, world) -> bool:
        # initialize result to False
        result = False

        # get references to actor and target from the world object
        actor = world.get_world_objects().get(self._actor_name,None)
        target = world.get_world_objects().get(self._target_name,None)

        # if either of the actor or target is not specified then return False
        if actor is None or target is None:
            return False
        else:
            # check if actor and target in the same room
            is_same_room = actor.get_room_name() == target.get_room_name()
            # check if actor and target in the required states
            is_actor_in_req_state = actor.get_current_state() == self._req_state.get(self._actor_name,None)
            is_target_in_req_state = target.get_current_state() == self._req_state.get(self._target_name,None)
            result = is_same_room && is_actor_in_req_state && is_target_in_req_state

        return result

