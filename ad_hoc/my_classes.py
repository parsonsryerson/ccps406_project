class World():
    def __init__(self, name: str, rooms:list = []) -> None:
        self.name = name
        self.rooms = rooms

    def __str__(self) -> str:
        result = f"{self.name}\n=====\nNumber of rooms: {len(self.rooms)}\n=====\n"
        for r in self.rooms.values():
            result += str(r) + '\n'
            for c in r.get_characters_in_room():
                result += str(c) + '\n'
            for i in r.get_items_in_room():
                result += str(i) + '\n'
        return result

    def add_rooms(self, rooms:dict) -> None:
        self.rooms.update(rooms)

    def get_rooms(self) -> set:
        return self.rooms


class Room:
    def __init__(self, name: str, state: dict, state_id: str) -> None:
        self.name = name
        self.state = state
        self.state_id = state_id
        self.description = state[state_id]['description']
        self.connections = {}
        self.characters_in_room = {}
        self.items_in_room = {}

    def __str__(self) -> str:
        return(f"{self.name}\n=====\nDescription: {self.description}\n=====\nNum Connections: {len(self.connections)}\nNum Characters: {len(self.characters_in_room)}\n")

    def add_connection(self, direction: str, connection) -> None:
        self.connections.update({direction:connection})

    def add_character(self, character) -> None:
        self.characters_in_room.update({character.get_name():character})

    def add_item(self, item) -> None:
        self.items_in_room.update({item.get_name():item})

    def get_connections(self) -> dict:
        return self.connections

    def get_characters_in_room(self) -> dict:
        return self.characters_in_room

    def get_items_in_room(self) -> dict:
        return self.items_in_room

    def get_description(self) -> str:
        return self.description

    def remove_connection(self,connection_name:str) -> None:
        self.connections.pop(connection_name)

    def remove_character(self,character) -> None:
        self.characters_in_room.pop(character.get_name())

    def remove_item(self,item) -> None:
        self.items_in_room.pop(item.get_name())


class Character():
    def __init__(self, name:str, state:dict, state_id:str, current_loc:str, is_playable:bool) -> None:
        self.name = name
        self.state = state
        self.state_id = state_id
        self.description = state[state_id]['description']
        self.current_loc = current_loc
        self.is_playable = is_playable
        self.inventory = {}
 
    def __str__(self) -> str:
        return(f"{self.name}\n=====\nDescription: {self.description}\nIs Playable? {self.is_playable}\n")

    def set_location(self, new_loc: str) -> None:
        self.current_loc = new_loc

    def get_location(self) -> str:
        return self.current_loc

    def add_to_inventory(self, item) -> None:
        self.inventory.update({item.name:item})

    def is_player(self) -> bool:
        return self.is_playable

    def get_name(self) -> str:
        return self.name


class Item():
    def __init__(self, name:str, state:dict, state_id:str, current_loc:str, can_be_picked_up:bool) -> None:
        self.name = name
        self.state = state
        self.state_id = state_id
        self.description = state[state_id]['description']
        self.current_loc = current_loc
        self.can_be_picked_up = can_be_picked_up
 
    def __str__(self) -> str:
        return(f"{self.name}\n=====\nDescription: {self.description}\n")

    def get_name(self) -> str:
        return self.name