class World():
    def __init__(self, name, rooms=[]):
        self.name = name
        self.rooms = rooms

    def __str__(self):
        result = f"{self.name}\n=====\nNumber of rooms: {len(self.rooms)}\n=====\n"
        for r in self.rooms:
            result += str(r) + '\n'
            for c in r.get_characters_in_room():
                result += str(c) + '\n'
            for i in r.get_items_in_room():
                result += str(i) + '\n'
        return result

    def add_rooms(self, rooms):
        self.rooms += list(rooms)

    def get_rooms(self):
        return self.rooms


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connections = set({})
        self.characters_in_room = set({})
        self.items_in_room = set({})

    def __str__(self):
        return(f"{self.name}\n=====\nDescription: {self.description}\n=====\nNum Connections: {len(self.connections)}\nNum Characters: {len(self.characters_in_room)}\n")

    def add_connection(self, connection):
        self.connections.add(connection)

    def add_character(self, character):
        self.characters_in_room.add(character)

    def add_item(self, item):
        self.items_in_room.add(item)

    def get_connections(self):
        return self.connections

    def get_characters_in_room(self):
        return self.characters_in_room

    def get_items_in_room(self):
        return self.items_in_room


class Character():
    def __init__(self, name, description, starting_loc, is_playable):
        self.name = name
        self.description = description
        self.starting_loc = starting_loc
        self.is_playable = is_playable
 
    def __str__(self):
        return(f"{self.name}\n=====\nDescription: {self.description}\nIs Playable? {self.is_playable}\n")


class Item():
    def __init__(self, name, description, starting_loc, can_be_picked_up):
        self.name = name
        self.description = description
        self.starting_loc = starting_loc
        self.can_be_picked_up = can_be_picked_up
 
    def __str__(self):
        return(f"{self.name}\n=====\nDescription: {self.description}\n")