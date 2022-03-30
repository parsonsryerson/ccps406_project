# import classes
import json
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

	vw = GameView()
	mdl = GameModel()
	ctrl = GameController(mdl,vw)

	# generate world and add objects and available actions to it
	my_world = World(world_objects=data['world_objects'], available_actions=data['actions'])

	### Start Game

	# accept commands in a permenent while loop
	cmd_input=''
	while(True):
		cmd_input = input("\nprompt: ")
		if str.lower(cmd_input) == 'q':
			break
		response = CommandParser(my_world, cmd_input)
		# send response to view

		# check for game over
		if my_world.is_game_over():
			break

	# output gameover screen
	vw.print_game_over()


if __name__ == '__main__':
    main()