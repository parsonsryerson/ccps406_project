# import classes
import json
import os
from game_model import *
from game_view import * 
from game_controller import *
from game_classes import *

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
	my_world = World(world_objects=data['world_objects'], available_actions=data['actions'], available_commands=commands_dict)

	vw = GameView()
	mdl = GameModel()
	ctrl = GameController(my_world, mdl, vw)

	### Start Game
	os.system('cls') # for windows
	os.system('clear') # for unix/mac
	ctrl.print_response('introduction')
	ctrl.print_response(CommandParser(my_world).try_parse('describe'))

	# accept commands in a permenent while loop
	cmd_input=''
	while(True):
		cmd_input = input("\n>>> ")
		if str.lower(cmd_input) == 'q':
			break
		response = CommandParser(my_world).try_parse(cmd_input)

		# send response to view
		ctrl.print_response(response)

		# check for game over
		if my_world.is_game_over():
			break

	# output gameover screen
	ctrl.print_response('game over')


if __name__ == '__main__':
    main()