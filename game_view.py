import os
import time

class GameView():

	def __init__(self, commands, responses):
		self._commands = commands
		self._responses = responses

	def clear_screen(self):
		os.system('cls') # for windows
		os.system('clear') # for unix/mac

	def print_help_commands(self):
		print(self._responses.get('help'))
		for command in sorted(self._commands.keys()):
			print(f"- {command}")

	def print_inventory(self, inventory = []):
		if len(inventory) == 0:
			print(self._responses.get('inventory'),get("=0"))
		else:
			print(self._responses.get('inventory'),get(">0"))
			for item in inventory:
				print(f"- {item}")

	def print_error(self, error_message):
		print(self._responses.get(error_message))

	def print_message_immediate(self, immediate_text):
		print(self._responses.get(immediate_text))

	def print_message_slow(self, slow_text):
		print("\n")
		for c in slow_text:
			print(c,end='',flush=True)
			time.sleep(0.01)
		print('')

	def get_command_map(self) -> dict:
		return self._commands



