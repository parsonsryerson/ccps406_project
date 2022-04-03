class CommandParser():

    # Constructor
    def __init__(self, world) -> None:
        self._world = world
        self._actor_name = world.get_player_name()
        self._action_name = None
        self._target_name = None
        self._ignore_tokens = ['on','at','from','to','the']

    def try_parse(self, command:str) -> str:
        # split the command
        available_commands = self._world.get_available_commands()
        split_text = []
        for x in command.split():
            next_token = str.lower(x)
            if next_token in available_commands.keys():
                next_token = available_commands.get(next_token).split()
            else:
                return 'error action'
            split_text.extend(next_token)
        split_text = list(dict.fromkeys(split_text))

        # print(f"DEBUG - CommandParser - command: {command}, split_text: {split_text}")
        assert(len(split_text) >= 1 and len(split_text) <= 2)
        self._action_name = split_text[0]
        self._target_name = split_text[1] if len(split_text) > 1 else None
        # print(f"DEBUG - CommandParser Class - split_text: {split_text}, action_name: {self._action_name}, target_name: {self._target_name}")
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
            rooms.update({room_name : Room(room_name,r['state']) for room_name,r in world_objects['rooms'].items()})
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
        self._current_state = 'free'
        self._description_length = 'long'

    # Setter Methods
    def set_current_state(self, next_state:str) -> None:
        self._current_state = next_state
        self._description_length = 'long'

    # Getter Methods
    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        # print(f"DEBUG - WorldObject - current_state: {self._current_state}, self._state: {self._state}")
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
    def __init__(self, name:str, state:dict) -> None:
        super().__init__(name,state)
        # override
        self._current_state = 'init'
        self._connections = self._state[self._current_state]['connections']
        self._game_objects = {}

    # Setter Methods

    # override
    def set_current_state(self, next_state:str) -> None:
        self._current_state = next_state
        self._description_length = 'long'
        self.set_connections(self._state[self._current_state]['connections'])

    def set_connections(self, connections:dict) -> None:
        self._connections.update(connections)

    def set_game_objects(self, game_objects:dict) -> None:
        # print(f"DEBUG - Room Class - room name: {self._name}, game_objects added: {game_objects}")
        self._game_objects.update(game_objects)

    def remove_game_objects(self, game_object_key:str) -> None:
        # print(f"DEBUG - Room Class - room name: {self._name}, game_objects removed: {game_object_key}")
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
        # print(f"DEBUG - GameObject Class - name: {self._name}, old room: {self._current_room_name}, new room: {room_name}")
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
        if self._name in ['bread','cheese','chocolate','grapes','key','hourglass']:
            self.set_current_state('hidden')

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
    def __init__(self, world, action_name:str, actor_name:str, target_name:str) -> None:
        self._world = world
        self._action_name = action_name
        self._actor_name = actor_name
        self._target_name = target_name
        # print(f"DEBUG - Action Constructor - action_name: {action_name}, actor_name: {actor_name}, target_name: {target_name}")
        if target_name is not None and action_name != 'describe':
            self._req_state = self._world.get_available_actions().get(self._action_name).get(self._target_name).get('req_state')
            self._next_state = self._world.get_available_actions().get(self._action_name).get(self._target_name).get('next_state')
            self._description_success = self._world.get_available_actions().get(self._action_name).get(self._target_name).get('description_success')
        else:
            self._req_state = {}
            self._next_state = {}
            self._description_success = ''
        # print(f"DEBUG - Action Constructor - req_state: {self._req_state}, next_state: {self._next_state}, description_success: {self._description_success}")

    def perform_action(self) -> str:
        # initialize result to empty string
        result = ''

        # special case - "help" action simply returns help - no changes to game world or state
        if self._action_name in ["help","inventory"]:
            result = self._action_name
        # special case - "describe" action always meets conditions
        elif self._action_name == "describe":
            result = self.__perform_describe()
        # special case - "move" action requires different conditions
        elif self._action_name == "move":
            result = self.__perform_move()

        # general case - check if conditions for actions are met, if so update states and return success description
        elif self.__meets_conditions():
            # print(f"DEBUG - Action Class - met general case conditions")
            self.__update_states()
            # print(f"DEBUG - Action Class - after update states")
            self.__update_inventory()
            result = self._description_success
            # print(f"DEBUG - Action __meets_conditions - self._req_state: {self._req_state}, self._next_state: {self._next_state}")
            if 'room' in self._req_state.keys() and 'room' in self._next_state.keys():
                if 'init' in self._req_state.get('room') and self._next_state.get('room') == 'free':
                    result += '\n'+self._world.get_rooms().get(self._world.get_characters().get(self._actor_name).get_room_name()).get_description()
            # print(f"DEBUG - Action Class - result: {result}")
        return result

    def __perform_describe(self) -> str:
        # if no target specified, assume target is current room of player
        if self._target_name is None:
            self._target_name = self._world.get_characters().get(self._world.get_player_name()).get_room_name()
        
        if self._target_name in self._world.get_rooms():
            target = self._world.get_rooms().get(self._target_name)
            # print(f"DEBUG - Action __perform_describe - target: {target}")
            result = target.get_description()
            # check for free items in the room
            free_items_in_room = {}
            for obj_name,obj in target.get_game_objects().items():
                if obj.get_current_state() == "free" and obj_name != self._world.get_player_name():
                    free_items_in_room.update({obj_name:obj})
            # print(f"DEBUG - Action __perform_describe - free_items_in_room: {free_items_in_room}")
            if len(free_items_in_room) > 0:
                for item_name,item in free_items_in_room.items():
                    result += '\nOn the floor, there is '+item.get_description()

            # check for connections to other rooms
            if len(target.get_connections()) > 0:
                directions = list(target.get_connections().keys())
                if len(target.get_connections()) == 1:
                    result += f'\nYou can see a passage to the {directions[0]}.'
                else:
                    result += f'\nYou can see passages to the {directions[0]}'
                    for direction in directions[1:-1]:
                        result += f'{direction}, '
                    result += f' and {directions[-1]}.'
            return result
        elif self._target_name in self._world.get_characters():
            return self._world.get_characters().get(self._target_name).get_description()
        elif self._target_name in self._world.get_items():
            return self._world.get_items().get(self._target_name).get_description()
        else:
            return None

    def __perform_move(self) -> str:
        # translate the name of the target into the correct room name based on the actor's current location
        prev_room_name = self._world.get_characters().get(self._actor_name).get_room_name()
        next_room_name = self._world.get_rooms().get(prev_room_name).get_connections().get(self._target_name)
        if next_room_name is None:
            return "error room"
        # print(f"DEBUG - Action Class - prev_room_name: {prev_room_name}, next_room_name: {next_room_name}")
        # update the actor's location to the next room - and its inventory
        # print(f"DEBUG - Action Class - Before room update: {self._world.get_characters().get(self._actor_name).get_room_name()}")
        self._world.get_characters().get(self._actor_name).set_room_name(next_room_name)
        for inv_item_name,inv_item in self._world.get_characters().get(self._actor_name).get_inventory().items():
            inv_item.set_room_name(next_room_name)
        # print(f"DEBUG - Action Class - After room update: {self._world.get_characters().get(self._actor_name).get_room_name()}")
        # update the previous and next room's game objects
        self._world.get_rooms().get(prev_room_name).remove_game_objects(self._actor_name)
        self._world.get_rooms().get(next_room_name).set_game_objects({self._actor_name:self._world.get_characters().get(self._actor_name)})
        # return description of next room
        self._target_name = next_room_name
        # update book state
        self._world.get_items().get('book').set_current_state('inventory '+next_room_name)
        return self.__perform_describe()

    def __update_states(self) -> None:
        # print(f"DEBUG - Action __update_states - self._next_state: {self._next_state}, self._target_name: {self._target_name}")
        for name, next_state in self._next_state.items(): 
            # world_object = self._world.get_world_objects().get(name,None)
            if name == 'actor':
                world_object = self._world.get_characters().get(self._actor_name)
            elif name == 'target':
                if self._target_name in self._world.get_characters().keys():
                    world_object = self._world.get_characters().get(self._target_name)
                elif self._target_name in self._world.get_items().keys():
                    world_object = self._world.get_items().get(self._target_name)
            elif name == 'room':
                actor = self._world.get_characters().get(self._actor_name)
                world_object = self._world.get_rooms().get(actor.get_room_name())
            elif name in self._world.get_characters().keys():
                world_object = self._world.get_characters().get(name)
            elif name in self._world.get_items().keys():
                world_object = self._world.get_items().get(name)
            # print(f"DEBUG - Action __update_states - name: {name}, next_state: {next_state}, world_object: {world_object}")
            if world_object is not None:
                world_object.set_current_state(next_state)

    def __update_inventory(self) -> None:
        if self._target_name in self._world.get_items().keys():
            actor = self._world.get_characters().get(self._actor_name)
            item = self._world.get_items().get(self._target_name)
            if 'inventory' in item.get_current_state():
                item.add_inventory_of(actor)
                actor.add_to_inventory({self._target_name:item})
            elif 'consumed' in item.get_current_state() or self._action_name in ['drop']:
                item.remove_inventory_of()
                actor.remove_from_inventory({self._target_name:item})

    def __meets_conditions(self) -> bool:
        # initialize result to False
        result = False

        # get references to actor and target from the world object
        # actor = world.get_world_objects().get(self._actor_name,None)
        actor = self._world.get_characters().get(self._world.get_player_name())
        if self._target_name in self._world.get_rooms():
            target = self._world.get_rooms().get(self._target_name)
        elif self._target_name in self._world.get_characters():
            target = self._world.get_characters().get(self._target_name)
        elif self._target_name in self._world.get_items():
            target = self._world.get_items().get(self._target_name)
        else:
            target = None

        # if either of the actor or target is not specified then return False
        if actor is None or target is None:
            return False
        else:
            # check if actor and target in the same room
            # print(f"DEBUG - Action State - actor: {actor}, target: {target}")
            # print(f"DEBUG - Action State - actor_room: {actor.get_room_name()}, target_room: {target.get_room_name()}")
            is_same_room = actor.get_room_name() == target.get_room_name()
            # check if actor and target in the required states
            actor_req_state = self._req_state.get("actor",None)
            target_req_state = self._req_state.get("target",None)
            # print(f"DEBUG - Action State - actor_req_state: {actor_req_state}, actor_curent_state: {actor.get_current_state()}")
            # print(f"DEBUG - Action State - target_req_state: {target_req_state}, target_current_state: {target.get_current_state()}")
            is_actor_in_req_state = (actor_req_state is None) or (actor.get_current_state() in actor_req_state)
            is_target_in_req_state = (target_req_state is None) or (target.get_current_state() in target_req_state)
            # print(f"DEBUG - Action Meets Conditions - is_same_room: {is_same_room}, is_actor_in_req_state: {is_actor_in_req_state}, is_target_in_req_state: {is_target_in_req_state}")
            result = is_same_room and is_actor_in_req_state and is_target_in_req_state

        return result

    # Getter Functions
    def get_req_state(self, name, actor, target):
        return self._req_state

    def get_next_state(self, name, actor, target):
        return self._next_state

    def get_description_success(self,name,actor,target):
        return self._description_success

