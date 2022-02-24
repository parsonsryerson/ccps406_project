###############################################################
#################### Import Relevant Files ####################
###############################################################

from my_classes import World, Room, Item, Character
import json

###############################################################
##################### Set Global Variables ####################
###############################################################

assets_file_name = 'assets.json'
commands_file_name = 'commands.json'
ignore_tokens = ['on','at','from','to','the']

# load game data from file to dictionary
with open(assets_file_name) as json_file:
    data = json.load(json_file)

# load acceptable commands from file to dictionary
with open(commands_file_name) as json_file:
    commands_dict = json.load(json_file)

###############################################################
#################### World Building Section ###################
###############################################################

# create characters
if 'characters' in data.keys():
	characters = [Character(x['name'],x['state'],"0",x['current_loc'],x['is_playable']) for x in data['characters']]
	player = [x for x in characters if x.is_player()][0]

# create items
if 'items' in data.keys():
	items = [Item(x['name'],x['state'],"0",x['current_loc'],x['can_be_picked_up']) for x in data['items']]

# create rooms
if 'rooms' in data.keys():
	rooms = {}
	connections = {}
	for x in data['rooms']:
		rooms[x['name']] = Room(x['name'],x['state'],"0")
		connections[x['name']] = x['connections']

# add connections, items and characters to rooms
for room in rooms.values():
	# connect rooms
	for direction, connection in connections[room.name].items():
		room.add_connection(direction,connection)
	# add characters and items to rooms
	for character in characters:
		if room.name == character.current_loc:
			room.add_character(character)
	# add items to rooms
	for item in items:
		if room.name == item.current_loc:
			room.add_item(item)

# generate world and add rooms to it
my_world = World(name='my_world', rooms=rooms)

# print summary of world, descriptions of each room, character and item
# print(my_world)

###############################################################
####################### Helper Functions ######################
###############################################################

def parse_input(input_text:str) -> dict:
	split_text = [str.lower(x) for x in input_text.split()]
	result = {}
	while len(split_text) > 0:
		if 'action' not in result.keys():
			result, split_text = get_action_command(result, split_text)
		elif 'target1' not in result.keys():
			result, split_text = get_target_command(result, split_text, 1)
		elif 'target2' not in result.keys():
			result, split_text = get_target_command(result, split_text, 2)
		else:
			split_text.pop(0)
	return result

def get_action_command(result:dict, split_text:list) -> tuple[dict, list]:
	while 'action' not in result.keys():
		if len(split_text) == 0:
			print("ERROR - action command not found.")
			break
		token = split_text[0]
		if token in commands_dict['actions'].keys():
			result.update(commands_dict['actions'][token])
			split_text.pop(0)
		elif token in ignore_tokens:
			split_text.pop(0)
		else:
			if len(split_text) > 1:
				split_text[0] += split_text[1]
			else:
				split_text.pop(0)
	return result, split_text

def get_target_command(result:dict, split_text:list,target_num:int) -> tuple[dict, list]:
	while 'target' not in result.keys():
		if len(split_text) == 0:
			print(f"ERROR - target {target_num} not found.")
			break
		token = split_text[0]
		if token in commands_dict['targets'].keys():
			target_result = commands_dict['targets'][token]
			target_result['target'+str(target_num)] = target_result.pop('target')
			result.update(target_result)
			split_text.pop(0)
		elif token in ignore_tokens:
			split_text.pop(0)
		else:
			if len(split_text) > 1:
				split_text[0] += split_text[1]
			else:
				split_text.pop(0)

	return result, remaining_text

def process_command(command:dict) -> None:
	# takes in a dictionary of {'action': x, 'target1':y, ['target2':z]}
	# this function should choose the appropriate objects to action and if needed, update state
	if 'action' not in command.keys():
		print("Did not understand command. Say 'help' for list of command words.")
		return None
	print(command)

	if command['action'] in ['help']:
		print("List of possible commands:\n")
		for k in commands_dict['actions'].keys():
			print(k)

	if command['action'] in ['describe']:
		print(my_world.get_rooms()[player.get_location()].get_description())

	if command['action'] in ['move']:
		# identify room player current in, check connections dict to see if target1 has a connection available in the direction
		current_room = player.get_location()
		next_room = my_world.get_rooms()[current_room].get_connections().get(command['target1'],None)

		if next_room is not None:
			# if so, remove player from current room, add them to new room, and update the current_loc for the player
			player.set_location(next_room)
			my_world.get_rooms()[current_room].remove_character(player)
			my_world.get_rooms()[next_room].add_character(player)
	return None

###############################################################
##################### Interactive Section #####################
###############################################################

# accept commands in a permenent while loop
cmd_input=''
while(True):
	cmd_input = input("\nprompt: ")
	if str.lower(cmd_input) == 'q':
		break
	process_command(parse_input(cmd_input))
