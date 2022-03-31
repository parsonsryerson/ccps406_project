class GameView():

	def __init__(self):
		pass

	def print_help_commands(self, available_actions):
		print("\n********************************************")
		print("************** HELP COMMANDS ***************")
		print("********************************************\n")
		print("AVAILABLE ACTIONS:\n")
		for action in available_actions:
			print(f"- {action}")

	def print_error_no_room_connection(self):
		print("You can't go that way.\n")

	def print_error_unavailable_action(self):
		print("You can't do that.\n")

	def print_error_unknown_target(self):
		print("Not sure what that is.\n")

	def print_description(self, output_text):
		print(f"{output_text}\n")

	def print_game_over(self):
		print("\n********************************************")
		print("*************** GAME OVER ******************")
		print("********************************************\n")

