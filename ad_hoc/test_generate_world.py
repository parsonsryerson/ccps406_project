from my_classes import World, Room, Item, Character
import json

# load game data from file to dictionary
with open('assets.json') as json_file:
    data = json.load(json_file)

# create characters
if 'characters' in data.keys():
	characters = [Character(x['name'],x['description'],x['starting_loc'],x['is_playable']) 
				  for x in data['characters']]

# create items
if 'items' in data.keys():
	items = [Item(x['name'],x['description'],x['starting_loc'],x['can_be_picked_up']) 
				  for x in data['items']]

# create rooms
if 'rooms' in data.keys():
	rooms = []
	connections = {}
	for x in data['rooms']:
		r = Room(x['name'], x['description'])
		rooms += [r]
		connections[x['name']] = x['connections']

# add connections, items and characters to rooms
for room in rooms:
	# connect rooms
	for connection in connections[room.name]:
		room.add_connection(connection)
	# add characters and items to rooms
	for character in characters:
		if room.name == character.starting_loc:
			room.add_character(character)
	# add items to rooms
	for item in items:
		if room.name == item.starting_loc:
			room.add_item(item)

# generate world and add rooms to it
my_world = World(name='my_world', rooms=rooms)

# print summary of world, descriptions of each room, character and item
print(my_world)