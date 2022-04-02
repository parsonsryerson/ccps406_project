import time

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

	def print_inventory(self, inventory = []):
		if len(inventory) == 0:
			print("You're not holding anything.")
			return None
		print("Currently in your inventory:\n")
		for item in inventory:
			print(f"- {item}")

	def print_error_no_room_connection(self):
		print("\nYou can't go that way.")

	def print_error_unavailable_action(self):
		print("\nYou can't do that.")

	def print_error_unknown_target(self):
		print("\nNot sure what that is.")

	def print_description(self, output_text):
		# print(f"\n{output_text}")
		print("\n")
		for c in output_text:
			print(c,end='',flush=True)
			time.sleep(0.01)
		print('')

	def print_introduction(self):
		print("\n********************************************")
		print("*************** WELCOME TO *****************")
		print("************ ~~ THE CIRCLES ~~ *************")
		print("********************************************\n")
		print("- For available commands, type 'help'")
		print("- To exit the game, type 'q'")

	def print_game_over(self):
		print("\n********************************************")
		print("*************** GAME OVER ******************")
		print("********************************************\n")

