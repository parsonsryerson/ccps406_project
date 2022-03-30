# import classes
import json
import game_model, game_view, game_controller
from game_classes import World

# constants
# assets_file_name = 'game_assets.json'
# commands_file_name = 'game_commands.json'
assets_file_name = 'game_assets_simple.json'
commands_file_name = 'game_commands_simple.json'
responses_file_name = 'game_responses.json'

def main():
	### Load Game Assets and Commands

	# load game data from file to dictionary
	with open(assets_file_name) as json_file:
	    data = json.load(json_file)

	# load acceptable commands from file to dictionary
	with open(commands_file_name) as json_file:
	    commands_dict = json.load(json_file)

	# load acceptable responses from file to dictionary
	with open(responses_file_name) as json_file:
	    responses_dict = json.load(json_file)

	### Initialize World

	# generate world and add objects and available actions to it
	my_world = World(world_objects=data['world_objects'], available_actions=data['actions'])

	### Start Game

	# accept commands in a permenent while loop
	cmd_input=''
	while(True):
		cmd_input = input("\nprompt: ")
		# check for game over
		# tbd
		if str.lower(cmd_input) == 'q':
			break
		response = CommandParser(world_objects,cmd_input)
		# send response to view

	
	# output gameover screen


if __name__ == '__main__':
    main()