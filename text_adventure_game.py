# import classes
import json
from game_model import *
from game_view import * 
from game_controller import *

# constants
assets_file_name = 'game_assets.json'
commands_file_name = 'game_command_map.json'
responses_file_name = 'game_responses.json'

def main():
	### Load Game Assets and Commands
	with open(assets_file_name) as json_file:
	    data = json.load(json_file)

	with open(commands_file_name) as json_file:
	    commands = json.load(json_file)

	with open(responses_file_name) as json_file:
	    responses = json.load(json_file)

	### Initialize World
	ctrl = GameController(GameModel(data), GameView(commands, responses))

	### Start Game
	ctrl.clear_screen()
	ctrl.print_response('introduction')
	ctrl.print_response(ctrl.try_parse('describe'))

	while(True):
		# accept commands in a permenent while loop
		cmd_input = input("\n>>> ")
		if ctrl.is_exit_command(cmd_input):
			break

		# try parsing command
		ctrl.print_response(ctrl.try_parse(cmd_input))

		# check for game over after action
		if ctrl.is_game_over():
			break

	# output gameover screen
	ctrl.print_response('game over')

if __name__ == '__main__':
    main()