from game_model import *
from game_view import * 
from game_controller import *
from game_classes import *

class GameController():

    def __init__(self, world, game_model, game_view):
        self._world = world
        self._game_model = game_model
        self._game_view = game_view

    def print_response(self, response):
        if 'error' in response and len(response.split()) > 1:
            error_type = response.split()[1]
            if error_type == 'room':
                self._game_view.print_error_no_room_connection()
            elif error_type == 'action':
                self._game_view.print_error_unavailable_action()
            elif error_type == 'target':
                self._game_view.print_error_unknown_target()
        elif response == 'help':
            self._game_view.print_help_commands(sorted(self._world.get_available_actions().keys()))
        elif response == 'game over':
            self._game_view.print_game_over()
        else:
            self._game_view.print_description(response)
