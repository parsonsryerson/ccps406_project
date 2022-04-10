from game_model import *
from game_view import * 
from game_classes import *

class GameController():
    _instance = None

    @staticmethod
    def get_instance(game_model, game_view):
        if GameController._instance is None:
            GameController(game_model, game_view)
        return GameController._instance

    def __init__(self, game_model, game_view) -> None:
        if GameController._instance is not None:
            raise Exception("This class is a Singleton")
        else:
            GameController._instance = self
            self._game_model = game_model
            self._game_view = game_view

    def clear_screen(self) -> None:
        self._game_view.clear_screen()

    def is_exit_command(self, command:str) -> bool:
        return True if str.lower(command) in ['q','quit','exit'] else False

    def is_game_over(self):
        return self._game_model.is_game_over()

    def print_response(self, response) -> None:
        if response == '' or response is None:
            pass
        elif 'error' in response.split()[0] and len(response.split()) > 1:
            if response.split()[1] in ['room','action','target']:
                self._game_view.print_error(response)
            else:
                pass
        elif response == 'help':
            self._game_view.print_help_commands(self._game_model.get_available_actions())
        elif response == 'inventory':
            player = self._game_model.get_characters().get(self._game_model.get_player_name())
            self._game_view.print_inventory(player.get_inventory())
        elif response in ['introduction','game over']:
            self._game_view.print_message_immediate(response)
        else:
            self._game_view.print_message_slow(response)

    def try_parse(self, command:str) -> str:
        result = ''

        # try parsing the input command - returns a response code and an Action() object
        (response, action) = self.parse_command(command)

        if response != 'success':
            # if command was unsuccessfully parsed, return error code
            result = response
        else: 
            # if command was successfully parsed, perform action based on action_name
            action_name = action.get_action_name()
            target_name = action.get_target_name()
            player = self._game_model.get_world_objects().get(self._game_model.get_player_name())
            all_rooms = self._game_model.get_rooms()
            current_room = all_rooms.get(player.get_room_name())

            if action_name in ["help","inventory"]:
                # special case - 'help' and 'inventory' are keywords which are understood further downstream
                result = action_name

            elif action_name == "describe":
                # special case - 'describe' conditions are always true and never updates state
                # if no target specified, assume target is current room of player
                if target_name is None:
                    action.set_target_name(current_room.get_room_name())
                result = self.perform_describe(action)

                # if the target of the describe command was a room, also check for free objects and connections
                if action.get_target_name() in all_rooms.keys():
                    result += self.describe_free_objects(action)
                    result += self.describe_room_connections(action)

            elif action_name == "move":
                # special case
                result = self.perform_move(action)

                # update book state each time player changes rooms
                self._game_model.get_world_objects().get('book').set_current_state('inventory '+player.get_room_name())

            else:
                # general case - may result in change of state
                result = self.perform_action(action) 

                # if general case unlocks a room, also add the new room description to the result
                if action.get_next_state().get('room','') == 'free':
                    result += '\n'+current_room.get_description()
        return result

    def parse_command(self, command:str):
        # split the command
        split_text = []
        command_map = self._game_view.get_command_map()
        available_actions = self._game_model.get_available_actions()

        # null case
        if command is None or command == '':
            return ('',Action(available_actions))


        for idx,x in enumerate(command.split()):
            next_token = str.lower(x)
            if next_token in command_map.keys():
                next_token = command_map.get(next_token).split()
            elif idx==0:
                return ('error action',Action(available_actions))
            else:
                return ('error target',Action(available_actions))
            split_text.extend(next_token)
        split_text = list(dict.fromkeys(split_text))

        action_name = split_text[0]
        target_name = split_text[1] if len(split_text) > 1 else None
        actor_name = self._game_model.get_player_name()
        return ('success', Action(available_actions, action_name, actor_name, target_name))

    def perform_action(self, action) -> str:
        # check if conditions for actions are met
        if self.__meets_conditions(action):
            # update state of objects involved in the action
            self.__update_states(action)
            # update inventory of objects involved in the action
            self.__update_inventory(action)
            # return the result of the action succeeding
            result = action.get_description_success()
        else:
            result = 'error target'
        return result

    def perform_describe(self, action) -> str:
        player = self._game_model.get_world_objects().get(self._game_model.get_player_name())
        target = self._game_model.get_world_objects().get(action.get_target_name())

        # Add description of target to result if in the same room
        if player.get_room_name() == target.get_room_name():
            return target.get_description()
        else:
            return 'error target'

    def describe_free_objects(self, action) -> str:
        # check for free items in the room
        result = ''
        target = self._game_model.get_world_objects().get(action.get_target_name())
        for obj_name,obj in target.get_game_objects().items():
            if obj.get_current_state() == "free" and obj_name != self._game_model.get_player_name():
                result += '\nIn the room, there is '+obj.get_description()
        return result

    def describe_room_connections(self, action) -> str:
        # check for connections to other rooms
        result = ''
        target = self._game_model.get_world_objects().get(action.get_target_name())
        if len(target.get_connections()) > 0:
            directions = list(target.get_connections().keys())
            if len(target.get_connections()) == 1:
                result += f'\nYou can see a passage to the {directions[0]}.'
            else:
                result += f'\nYou can see passages to the {directions[0]}'
                for direction in directions[1:-1]:
                    result += f'{direction}, '
                result += f' and {directions[-1]}.'
        return result

    def perform_move(self, action) -> str:
        # translate the name of the target into the correct room name based on the actor's current location
        actor = self._game_model.get_world_objects().get(action.get_actor_name())
        prev_room = self._game_model.get_world_objects().get(actor.get_room_name())
        next_room_name = prev_room.get_connections().get(action.get_target_name())
        next_room = self._game_model.get_world_objects().get(next_room_name)
        if next_room is None:
            return "error room"

        # update the actor's location to the next room - and its inventory
        actor.set_room_name(next_room_name)
        for inv_item_name, inv_item in actor.get_inventory().items():
            inv_item.set_room_name(next_room_name)

        # update the previous and next room's game objects
        prev_room.remove_game_objects(action.get_actor_name())
        next_room.set_game_objects({action.get_actor_name():actor})

        # return description of next room
        action.set_target_name(next_room_name)
        return self.perform_describe(action)

    def __meets_conditions(self, action) -> bool:
        actor = self._game_model.get_world_objects().get(self._game_model.get_player_name())
        target = self._game_model.get_world_objects().get(action.get_target_name())

        if actor is None or target is None:
            # if either of the actor or target is not specified then return False
            return False
        else:
            # check if actor and target in the same room
            is_same_room = actor.get_room_name() == target.get_room_name()

            # check if actor and target in the required states
            actor_req_state = action.get_req_state().get("actor")
            target_req_state = action.get_req_state().get("target")
            is_actor_in_req_state = (actor_req_state is None) or (actor.get_current_state() in actor_req_state)
            is_target_in_req_state = (target_req_state is None) or (target.get_current_state() in target_req_state)

            return is_same_room and is_actor_in_req_state and is_target_in_req_state

    def __update_states(self, action) -> None:
        actor = self._game_model.get_world_objects().get(action.get_actor_name())

        for name, next_state in action.get_next_state().items(): 
            if name in self._game_model.get_world_objects().keys():
                world_object = self._game_model.get_world_objects().get(name)
            elif name == 'target':
                world_object = self._game_model.get_world_objects().get(action.get_target_name())
            elif name == 'actor':
                world_object = actor
            elif name == 'room':
                world_object = self._game_model.get_rooms().get(actor.get_room_name())

            world_object.set_current_state(next_state)

    def __update_inventory(self, action) -> None:
        if action.get_target_name() in self._game_model.get_game_objects().keys():
            actor = self._game_model.get_game_objects().get(action.get_actor_name())
            item = self._game_model.get_game_objects().get(action.get_target_name())
            if 'inventory' in item.get_current_state():
                item.add_inventory_of(actor)
                actor.add_to_inventory({action.get_target_name():item})
            elif 'consumed' in item.get_current_state() or action.get_action_name() in ['drop']:
                item.remove_inventory_of()
                actor.remove_from_inventory({action.get_target_name():item})
