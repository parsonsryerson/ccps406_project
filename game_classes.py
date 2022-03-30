class CommandParser():

    # Constructor
    def __init__(self, world, input_string:str = '') -> None:
        self._input_string = input_string
        self._actor_name = world.get_player_name()
        self._action_name = None
        self._target_name = None
        self._ignore_tokens = ['on','at','from','to','the']

    def try_parse(self, world, command:str) -> str:
        parse_result = self.parse_command(world,command)
        if parse_result == "success":
            # get required parameters to create an Action
            action_params = world.get_available_actions().get(self._action_name).get(self._target_name)
            action = Action(
                name = self._action_name,
                actor_name = self._actor_name, 
                target_name = self._target_name, 
                req_state = action_params['req_state'], 
                next_state = action_params['next_state'], 
                description_success = action_params['description_success']
            )
            action_result = action.perform_action(world)
        else:
            action_result = parse_result
        return action_result



    # Translates input string into three key aspects
    # - Actor - the object performing the action
    # - Action - the action being performed
    # - Target - the object the action is being performed on
    # Returns the phrase to send to the view. 
    # - If successful, this is an action desription
    # - If one of action or target can't be found, then sends appropriate error message.
    def parse_command(self, world, command_dict:dict, command: str) -> str:
        ## parse the command
        split_text = [command_dict.get(str.lower(x),'') for x in command.split()]
        while len(split_text) > 0:
            if self._action_name is None:
                action_name, split_text = self.__find_action_name(world, split_text)
                if action_name is not None:
                    self.__set_action_name(action_name)
                else:
                    print("error - action")
                    break
            elif self._target_name is None:
                target_name, split_text = self.__find_target_name(world, split_text)
                if target_name is not None:
                    self.__set_target_name(target)
                else:
                    print("error - target")
                    break
            else:
                return "success"

    def __find_action_name(self, world, split_text:[]):
        while(self._action_name is None):
            if len(split_text) == 0:
                break
            token = split_text[0]
            if token in world.get_available_actions().keys():
                split_text.pop(0)
                return token, split_text
            elif token in self._ignore_tokens:
                split_text.pop(0)
            else:
                if len(split_text) > 1:
                    split_text[0] += split_text[1]
                else:
                    split_text.pop(0)
        return None, split_text

    def __find_target_name(self, world, split_text:[]):
        while(self._target_name is None):
            if len(split_text) == 0:
                break
            token = split_text[0]
            if token in world.get_world_objects().keys():
                split_text.pop(0)
                return token, split_text
            elif token in self._ignore_tokens:
                split_text.pop(0)
            else:
                if len(split_text) > 1:
                    split_text[0] += split_text[1]
                else:
                    split_text.pop(0)
        return None, split_text

    # Setter Methods (private)
    def __set_action_name(self, action_name: str) -> None:
        self._action_name = action_name

    def __set_actor_name(self, actor) -> None:
        self._actor_name = actor_name

    def __set_target_name(self, target) -> None:
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
    def __init__(self, world_objects:dict = {}, available_actions:dict = {}) -> None:
        self._world_objects = world_objects
        self._available_actions = available_actions
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
        for obj_dict in world_objects['characters']:
            if obj_dict.get('is_playable',False):
                return obj_dict.get('name',None)
        return ''

    # build world 
    def __build_characters(self, world_objects:dict) -> dict:
        characters = {}
        if 'characters' in world_objects.keys():
            characters.update(
                {c['name'] : Character(c['name'],c['state'],c['starting_room'],c['is_playable']) 
                for c in world_objects['characters']})
        return characters

    def __build_items(self, world_objects:dict) -> dict:
        items = {}
        if 'items' in world_objects.keys():
            items.update(
                {i['name'] : Item(i['name'],i['state'],i['starting_room'],i['is_carryable'],i['is_equippable']) 
                for i in world_objects['items']})
        return items

    def __build_rooms(self, world_objects:dict) -> dict:
        rooms = {}
        if 'rooms' in world_objects.keys():
            rooms.update({r['name'] : Room(r['name'],r['state'],r['connections']) for r in world_objects['rooms']})
        return rooms

    def __add_game_objects_to_rooms(self, game_objects:dict) -> None:
        for obj_name,obj in game_objects.items():
            self._rooms.get(obj.get_room_name(),None).set_game_objects({obj_name:obj})

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
    def __init__(self, name:str, state:dict, connections:dict) -> None:
        super().__init__(name,state)
        self._connections = connections
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
            result = self.__perform_describe(world)

        # general case - check if conditions for actions are met, if so update states and return success description
        if self.__meets_conditions(world):
            self.__update_states(world)
            result = self._description_success
        return result

    def __perform_describe(self, world) -> str:
        # if no target specified, assume target is current room of player
        if self._target_name is None:
            actor = world.get_world_objects().get(world.get_player_name(),None)
            target = world.get_world_objects().get(actor.get_room_name(),None)
        else:
            target = world.get_world_objects().get(self._target_name,None)
        return target.get_description()

    def __update_states(self, world) -> None:
        for name, next_state in self._next_state.items(): 
            world_object = world.get_world_objects().get(name,None)
            if world_object is not None:
                world_object.set_current_state(next_state)

    def __meets_conditions(self, world) -> bool:
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
            result = is_same_room and is_actor_in_req_state and is_target_in_req_state

        return result

    # Getter Functions
    def get_req_state(self, name, actor, target):
        return self._req_state

    def get_next_state(self, name, actor, target):
        return self._next_state

    def get_description_success(self,name,actor,target):
        return self._description_success

