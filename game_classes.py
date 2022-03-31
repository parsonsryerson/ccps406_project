class CommandParser():

    # Constructor
    def __init__(self, world) -> None:
        self._world = world
        self._actor_name = world.get_player_name()
        self._action_name = None
        self._target_name = None
        self._ignore_tokens = ['on','at','from','to','the']

    # helper function
    def flatten(self,t):
        return [item for sublist in t for item in sublist]

    def try_parse(self, command:str) -> str:
        split_text = self.flatten([self._world.get_available_commands().get(str.lower(x),'').split() for x in command.split()])
        assert(len(split_text) >= 1 and len(split_text) <= 2)
        self._action_name = split_text[0]
        self._target_name = split_text[1] if len(split_text) > 1 else None
        result = Action(self._world, self._action_name, self._actor_name, self._target_name).perform_action()
        return result

    # Setter Methods (private)
    def __set_action_name(self, action_name: str) -> None:
        self._action_name = action_name

    def __set_actor_name(self, actor_name) -> None:
        self._actor_name = actor_name

    def __set_target_name(self, target_name) -> None:
        self._target_name = target_name

    # Getter Methods (public)
    def get_action_name(self) -> str:
        return self._action_name

    def get_actor_name(self):
        return self._actor_name

    def get_target_name(self):
        return self._target_name





class World():

    # Constructor
    def __init__(self, world_objects:dict = {}, available_actions:dict = {}, available_commands:dict = {}) -> None:
        self._world_objects = world_objects
        self._available_actions = available_actions
        self._available_commands = available_commands
        self._is_game_over = False
        self._player_name = self.find_player_name(world_objects)
        self._characters = self.__build_characters(world_objects)
        self._items = self.__build_items(world_objects)
        self._rooms = self.__build_rooms(world_objects)

        # add game objects to rooms
        self.__add_game_objects_to_rooms(self._characters)
        self.__add_game_objects_to_rooms(self._items)

    # make player name directly available from world class for convenience
    def find_player_name(self,world_objects:dict) -> str:
        for char_name, character in world_objects['characters'].items():
            if character.get('is_playable',False):
                return char_name
        return ''

    # build world 
    def __build_characters(self, world_objects:dict) -> dict:
        characters = {}
        if 'characters' in world_objects.keys():
            characters.update(
                {char_name : Character(char_name,c['state'],c['starting_room'],c['is_playable']) 
                for char_name,c in world_objects['characters'].items()})
        return characters

    def __build_items(self, world_objects:dict) -> dict:
        items = {}
        if 'items' in world_objects.keys():
            items.update(
                {item_name : Item(item_name,i['state'],i['starting_room'],i['is_carryable'],i['is_equippable']) 
                for item_name,i in world_objects['items'].items()})
        return items

    def __build_rooms(self, world_objects:dict) -> dict:
        rooms = {}
        if 'rooms' in world_objects.keys():
            rooms.update({room_name : Room(room_name,r['state'],r['connections']) for room_name,r in world_objects['rooms'].items()})
        return rooms

    def __add_game_objects_to_rooms(self, game_objects:dict) -> None:
        for obj_name,obj in game_objects.items():
            self._rooms.get(obj.get_room_name(),None).set_game_objects({obj_name:obj})

    # Setter Methods
    def set_world_objects(self, world_objects: dict) -> None:
        self._world_objects.update(world_objects)

    def set_available_actions(self, available_actions:dict) -> None:
        self._available_actions.update(available_actions)

    def set_available_commands(self, available_commands:dict) -> None:
        self._available_commands.update(available_commands)    
    
    def set_game_over(self, game_over: bool) -> None:
        self._is_game_over = game_over
    
    # Getter Methods
    def get_world_objects(self) -> dict:
        return self._world_objects

    def get_characters(self) -> dict:
        return self._characters

    def get_items(self) -> dict:
        return self._items

    def get_rooms(self) -> dict:
        return self._rooms

    def get_available_actions(self) -> dict:
        return self._available_actions

    def get_available_commands(self) -> dict:
        return self._available_commands

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
        result = self._state.get(self._current_state).get('description').get(self._description_length,'')
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
    def __init__(self, name:str, state:dict, connections:dict) -> None:
        super().__init__(name,state)
        self._connections = connections
        self._game_objects = {}

    # Setter Methods
    def set_connections(self, connections:dict) -> None:
        self._connections.update(connections)

    def set_game_objects(self, game_objects:dict) -> None:
        print(f"DEBUG - Room Class - room name: {self._name}, game_objects added: {game_objects}")
        self._game_objects.update(game_objects)

    def remove_game_objects(self, game_object_key:str) -> None:
        print(f"DEBUG - Room Class - room name: {self._name}, game_objects removed: {game_object_key}")
        self._game_objects.pop(game_object_key)

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

    # Setter Method
    def set_room_name(self,room_name) -> None:
        print(f"DEBUG - GameObject Class - name: {self._name}, old room: {self._current_room_name}, new room: {room_name}")
        self._current_room_name = room_name

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
    def __init__(self, world, name:str, actor_name:str, target_name:str) -> None:
        self._world = world
        self._action_name = name
        self._actor_name = actor_name
        self._target_name = target_name
        self._req_state = self._world.get_available_actions().get(self._action_name).get('req_state')
        self._next_state = self._world.get_available_actions().get(self._action_name).get('next_state')
        self._description_success = self._world.get_available_actions().get(self._action_name).get('description_success')

    def perform_action(self) -> str:
        # initialize result to empty string
        result = ''

        # special case - "help" action simply returns help - no changes to game world or state
        if self._action_name == "help":
            result = self._name
        # special case - "describe" action always meets conditions
        elif self._action_name == "describe":
            result = self.__perform_describe()
        # special case - "move" action requires different conditions
        elif self._action_name == "move":
            result = self.__perform_move()

        # general case - check if conditions for actions are met, if so update states and return success description
        elif self.__meets_conditions():
            self.__update_states()
            result = self._description_success
        return result

    def __perform_describe(self) -> str:
        # if no target specified, assume target is current room of player
        if self._target_name is None:
            actor = self._world.get_characters().get(self._world.get_player_name(),None)
            target = self._world.get_rooms().get(actor.get_room_name(),None)
        else:
            if self._target_name in self._world.get_rooms():
                target = self._world.get_rooms().get(self._target_name)
            elif self._target_name in self._world.get_characters():
                target = self._world.get_characters().get(self._target_name)
            elif self._target_name in self._world.get_items():
                target = self._world.get_items().get(self._target_name)
            else:
                target = None
        return target.get_description()

    def __perform_move(self) -> str:
        # translate the name of the target into the correct room name based on the actor's current location
        prev_room_name = self._world.get_characters().get(self._actor_name).get_room_name()
        next_room_name = self._world.get_rooms().get(prev_room_name).get_connections().get(self._target_name)
        if next_room_name is None:
            return "error room"
        print(f"DEBUG - Action Class - prev_room_name: {prev_room_name}, next_room_name: {next_room_name}")
        # update the actor's location to the next room
        print(f"DEBUT - Action Class - Before room update: {self._world.get_characters().get(self._actor_name).get_room_name()}")
        self._world.get_characters().get(self._actor_name).set_room_name(next_room_name)
        print(f"DEBUT - Action Class - After room update: {self._world.get_characters().get(self._actor_name).get_room_name()}")
        # update the previous and next room's game objects
        self._world.get_rooms().get(prev_room_name).remove_game_objects(self._actor_name)
        self._world.get_rooms().get(next_room_name).set_game_objects({self._actor_name:self._world.get_characters().get(self._actor_name)})
        # return description of next room
        return self._world.get_rooms().get(next_room_name).get_description()

    def __update_states(self) -> None:
        for name, next_state in self._next_state.items(): 
            world_object = self._world.get_world_objects().get(name,None)
            if world_object is not None:
                world_object.set_current_state(next_state)

    def __meets_conditions(self) -> bool:
        # initialize result to False
        result = False

        # get references to actor and target from the world object
        # actor = world.get_world_objects().get(self._actor_name,None)
        actor = self._world.get_characters().get(self._world.get_player_name())
        for world_object_type, world_object in self._world.get_world_objects().items():
            if self._target_name in world_object.keys():
                target = world_object.get(self._target_name,None)

        # if either of the actor or target is not specified then return False
        if actor is None or target is None:
            return False
        else:
            # check if actor and target in the same room
            is_same_room = actor.get_room_name() == target.get_room_name()
            # check if actor and target in the required states
            is_actor_in_req_state = actor.get_current_state() == self._req_state.get(self._actor_name,None)
            is_target_in_req_state = target.get_current_state() == self._req_state.get(self._target_name,None)
            result = is_same_room and is_actor_in_req_state and is_target_in_req_state

        return result

    # Getter Functions
    def get_req_state(self, name, actor, target):
        return self._req_state

    def get_next_state(self, name, actor, target):
        return self._next_state

    def get_description_success(self,name,actor,target):
        return self._description_success

