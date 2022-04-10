from game_model import *
from game_view import * 
from game_controller import *
from game_classes import *

class GameController():

    def __init__(self, world, game_model, game_view):
        self._world = world
        self._game_model = game_model
        self._game_view = game_view

    def perform_action(self, action) -> str:
        # initialize result to empty string
        result = ''

        # special case - "help" action simply returns help - no changes to game world or state
        if action.get_action_name() in ["help","inventory"]:
            result = action.get_action_name()
        # special case - "describe" action always meets conditions
        elif action.get_action_name() == "describe":
            result = self.__perform_describe(action)
        # special case - "move" action requires different conditions
        elif action.get_action_name() == "move":
            result = self.__perform_move(action)

        # general case - check if conditions for actions are met, if so update states and return success description
        elif self.__meets_conditions(action):
            # print(f"DEBUG - Action Class - met general case conditions")
            self.__update_states(action)
            # print(f"DEBUG - Action Class - after update states")
            self.__update_inventory(action)
            result = action.get_description_success()
            # print(f"DEBUG - Action __meets_conditions - self._req_state: {self._req_state}, self._next_state: {self._next_state}")
            if 'room' in action.get_req_state().keys() and 'room' in action.get_next_state().keys():
                if 'init' in action.get_req_state().get('room') and action.get_next_state().get('room') == 'free':
                    result += '\n'+self._world.get_rooms().get(self._world.get_characters().get(action.get_actor_name()).get_room_name()).get_description()
            # print(f"DEBUG - Action Class - result: {result}")
        else:
            result = 'error target'
        return result

    def __perform_describe(self, action) -> str:
        # if no target specified, assume target is current room of player
        if action.get_target_name() is None:
            action.set_target_name(self._world.get_characters().get(self._world.get_player_name()).get_room_name())
        
        if action.get_target_name() in self._world.get_rooms():
            target = self._world.get_rooms().get(action.get_target_name())
            # print(f"DEBUG - Action __perform_describe - target: {target}")
            result = target.get_description()
            # check for free items in the room
            free_items_in_room = {}
            for obj_name,obj in target.get_game_objects().items():
                if obj.get_current_state() == "free" and obj_name != self._world.get_player_name():
                    free_items_in_room.update({obj_name:obj})
            # print(f"DEBUG - Action __perform_describe - free_items_in_room: {free_items_in_room}")
            if len(free_items_in_room) > 0:
                for item_name,item in free_items_in_room.items():
                    result += '\nOn the floor, there is '+item.get_description()

            # check for connections to other rooms
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
        elif action.get_target_name() in self._world.get_characters():
            player = self._world.get_characters().get(self._world.get_player_name())
            target = self._world.get_characters().get(action.get_target_name())
            if player.get_room_name() == target.get_room_name():
                return target.get_description()
            else:
                return 'error target'
        elif action.get_target_name() in self._world.get_items():
            player = self._world.get_characters().get(self._world.get_player_name())
            target = self._world.get_items().get(action.get_target_name())
            if player.get_room_name() == target.get_room_name():
                return target.get_description()
            else:
                return 'error target'
        else:
            return None

    def __perform_move(self, action) -> str:
        # translate the name of the target into the correct room name based on the actor's current location
        prev_room_name = self._world.get_characters().get(action.get_actor_name()).get_room_name()
        next_room_name = self._world.get_rooms().get(prev_room_name).get_connections().get(action.get_target_name())
        if next_room_name is None:
            return "error room"
        # print(f"DEBUG - Action Class - prev_room_name: {prev_room_name}, next_room_name: {next_room_name}")
        # update the actor's location to the next room - and its inventory
        # print(f"DEBUG - Action Class - Before room update: {self._world.get_characters().get(self._actor_name).get_room_name()}")
        self._world.get_characters().get(action.get_actor_name()).set_room_name(next_room_name)
        for inv_item_name,inv_item in self._world.get_characters().get(action.get_actor_name()).get_inventory().items():
            inv_item.set_room_name(next_room_name)
        # print(f"DEBUG - Action Class - After room update: {self._world.get_characters().get(self._actor_name).get_room_name()}")
        # update the previous and next room's game objects
        self._world.get_rooms().get(prev_room_name).remove_game_objects(action.get_actor_name())
        self._world.get_rooms().get(next_room_name).set_game_objects({action.get_actor_name():self._world.get_characters().get(action.get_actor_name())})
        # return description of next room
        action.set_target_name(next_room_name)
        # update book state
        self._world.get_items().get('book').set_current_state('inventory '+next_room_name)
        return self.__perform_describe()

    def __update_states(self, action) -> None:
        # print(f"DEBUG - Action __update_states - self._next_state: {self._next_state}, self._target_name: {self._target_name}")
        for name, next_state in action.get_next_state().items(): 
            # world_object = self._world.get_world_objects().get(name,None)
            if name == 'actor':
                world_object = self._world.get_characters().get(action.get_actor_name())
            elif name == 'target':
                if action.get_target_name() in self._world.get_characters().keys():
                    world_object = self._world.get_characters().get(action.get_target_name())
                elif action.get_target_name() in self._world.get_items().keys():
                    world_object = self._world.get_items().get(action.get_target_name())
            elif name == 'room':
                actor = self._world.get_characters().get(action.get_actor_name())
                world_object = self._world.get_rooms().get(actor.get_room_name())
            elif name in self._world.get_characters().keys():
                world_object = self._world.get_characters().get(name)
            elif name in self._world.get_items().keys():
                world_object = self._world.get_items().get(name)
            # print(f"DEBUG - Action __update_states - name: {name}, next_state: {next_state}, world_object: {world_object}")
            if world_object is not None:
                world_object.set_current_state(next_state)

    def __update_inventory(self, action) -> None:
        if action.get_target_name() in self._world.get_items().keys():
            actor = self._world.get_characters().get(action.get_actor_name())
            item = self._world.get_items().get(action.get_target_name())
            if 'inventory' in item.get_current_state():
                item.add_inventory_of(actor)
                actor.add_to_inventory({action.get_target_name():item})
            elif 'consumed' in item.get_current_state() or action.get_action_name() in ['drop']:
                item.remove_inventory_of()
                actor.remove_from_inventory({action.get_target_name():item})

    def __meets_conditions(self, action) -> bool:
        # initialize result to False
        result = False

        # get references to actor and target from the world object
        # actor = world.get_world_objects().get(self._actor_name,None)
        actor = self._world.get_characters().get(self._world.get_player_name())
        if action.get_target_name() in self._world.get_rooms():
            target = self._world.get_rooms().get(action.get_target_name())
        elif action.get_target_name() in self._world.get_characters():
            target = self._world.get_characters().get(action.get_target_name())
        elif action.get_target_name() in self._world.get_items():
            target = self._world.get_items().get(action.get_target_name())
        else:
            target = None

        # if either of the actor or target is not specified then return False
        if actor is None or target is None:
            return False
        else:
            # check if actor and target in the same room
            # print(f"DEBUG - Action State - actor: {actor}, target: {target}")
            # print(f"DEBUG - Action State - actor_room: {actor.get_room_name()}, target_room: {target.get_room_name()}")
            is_same_room = actor.get_room_name() == target.get_room_name()
            # check if actor and target in the required states
            actor_req_state = action.get_req_state().get("actor",None)
            target_req_state = action.get_req_state().get("target",None)
            # print(f"DEBUG - Action State - actor_req_state: {actor_req_state}, actor_curent_state: {actor.get_current_state()}")
            # print(f"DEBUG - Action State - target_req_state: {target_req_state}, target_current_state: {target.get_current_state()}")
            is_actor_in_req_state = (actor_req_state is None) or (actor.get_current_state() in actor_req_state)
            is_target_in_req_state = (target_req_state is None) or (target.get_current_state() in target_req_state)
            # print(f"DEBUG - Action Meets Conditions - is_same_room: {is_same_room}, is_actor_in_req_state: {is_actor_in_req_state}, is_target_in_req_state: {is_target_in_req_state}")
            result = is_same_room and is_actor_in_req_state and is_target_in_req_state

        return result



    def print_response(self, response):
        # print(f"DEBUG - In GameController - response : {response}")
        if response == '' or response is None:
            pass
        elif 'error' in response.split()[0] and len(response.split()) > 1:
            error_type = response.split()[1]
            # print(f"DEBUG - In GameController - error_type : {error_type}")
            if error_type == 'room':
                self._game_view.print_error_no_room_connection()
            elif error_type == 'action':
                self._game_view.print_error_unavailable_action()
            elif error_type == 'target':
                self._game_view.print_error_unknown_target()
        elif response == 'help':
            self._game_view.print_help_commands(sorted(self._world.get_available_actions().keys()))
        elif response == 'inventory':
            # print(f"DEBUG - GameController print_response - player: {self._world.get_characters().get(self._world.get_player_name())}")
            # print(f"DEBUG - GameController print_response - inventory: {self._world.get_characters().get(self._world.get_player_name()).get_inventory()}")
            self._game_view.print_inventory(self._world.get_characters().get(self._world.get_player_name()).get_inventory())
        elif response == 'introduction':
            self._game_view.print_introduction()
        elif response == 'game over':
            self._game_view.print_game_over()
        else:
            self._game_view.print_description(response)
