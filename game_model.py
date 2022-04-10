from game_classes import *

class GameModel():
    _instance = None

    @staticmethod
    def get_instance(data):
    	# Used to enforce Singleton
        if GameModel._instance is None:
            GameModel(data)
        return GameModel._instance

    # Constructor
    def __init__(self, data) -> None:
        if GameModel._instance is not None:
            raise Exception("This class is a Singleton")
        else:
            GameModel._instance = self
            self.__set_available_actions(data['actions'])
            self.__set_world_objects(data['world_objects'])
            self.__set_game_objects_to_rooms()
            self.__set_player_name()
            self.set_game_over(False)

    # Setter Methods
    def __set_available_actions(self, available_actions:dict) -> None:
    	self._available_actions = available_actions

    def __set_world_objects(self, world_objects:dict) -> None:
        self._world_objects = {}
        for obj_type, obj in world_objects.items():
            for name,x in world_objects.get('game_objects').items():
                if 'is_playable' in x.keys():
                    self._world_objects.update(
                    	{name : Character(name,x['state'],x['starting_room'],x['starting_state'],x['is_playable'])})
                elif 'is_carryable' in x.keys():
                    self._world_objects.update(
                    	{name : Item(name,x['state'],x['starting_room'],x['starting_state'],x['is_carryable'],x['is_equippable'])})
            for room_name,r in world_objects.get('rooms').items():
                self._world_objects.update({room_name : Room(room_name,r['state'],r['starting_state'])})

    def __set_game_objects_to_rooms(self) -> None:
        for obj_name,obj in self.get_game_objects().items():
            self.get_rooms().get(obj.get_room_name()).set_game_objects({obj_name:obj})

    def __set_player_name(self) -> None:
    	# make player name directly available from world class for convenience
        for name, game_obj in self.get_game_objects().items():
            if game_obj.get_is_player():
                self._player_name = name
    
    def set_game_over(self, game_over: bool) -> None:
        self._is_game_over = game_over
    
    # Getter Methods
    def get_world_objects(self) -> dict:
        return self._world_objects

    def get_game_objects(self) -> dict:
        return {k:v for k,v in self._world_objects.items() if isinstance(v,GameObject)}

    def get_characters(self) -> dict:
        return {k:v for k,v in self._world_objects.items() if isinstance(v,Character)}

    def get_items(self) -> dict:
        return {k:v for k,v in self._world_objects.items() if isinstance(v,Item)}

    def get_rooms(self) -> dict:
        return {k:v for k,v in self._world_objects.items() if isinstance(v,Room)}

    def get_available_actions(self) -> dict:
        return self._available_actions

    def get_player_name(self) -> str:
        return self._player_name

    def is_game_over(self) -> bool:
        return self._is_game_over
