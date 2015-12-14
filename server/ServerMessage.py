#!/usr/bin/env python

import logging

from common.Message import Message
from common.MessageEnum import MessageEnum
from common.PlayerEnum import PlayerEnum

from server.ServerModel import ServerModel

class ServerMessage:

    def __init__(self, output_queue):
        self._logger = logging.getLogger('ServerMessage')
        
        self._output_queue = output_queue
        
        self._server_model = ServerModel()
    
    # Handle the messages sent by the client (player)
    def handle_message(self, message_list, player):
        for message in message_list:
            message_enum = message.get_message_enum()
            #num_args = message.get_num_args()
            message_args = message.get_args()
            
            # Handle move message
            if message_enum == MessageEnum.MOVE and self.is_turn_character(player) == True:
                character = player.get_character()
                current_room = self._server_model.get_character_position(character)
                destination_room = message_args[0]
                
                valid_move = self._server_model.perform_move(character, destination_room)
                
                if valid_move == True:
                    new_room = self._server_model.get_character_position(character)
                    response_args = [True, character, current_room, new_room]
                    broadcast = True
                else:
                    response_args = [False]
                    broadcast = False
                
                return_message = Message(MessageEnum.MOVE, 1, response_args)
                
                self._output_queue.put((broadcast, return_message))
            
            # Handle suggestion begin message
            elif message_enum == MessageEnum.SUGGESTION_BEGIN and self.is_turn_character(player) == True:
                character = player.get_character()
                
                suspect = message_args[0]
                weapon = message_args[1]
                room = message_args[2]
                
                # Set the suggestion on the server
                self._server_model.set_suggestion([suspect, weapon, room])
                
                # Get the next suggest player
                self._server_model.set_suggester(character)
                
                # Attempt to disprove suggestion with next suggester
                self.perform_suggest()
            
            # Handle suggest message
            elif message_enum == MessageEnum.SUGGEST:
                disprove_character = player.get_character()
                
                player_enum = message_args[0]
                weapon = message_args[1]
                room = message_args[2]
                
                # Player disproved the suggestion
                if player_enum is not None or weapon is not None or room is not None:
                    response_args = [disprove_character, player_enum, weapon, room]
                    return_message = Message(MessageEnum.SUGGESTION_END, 1, response_args)
                    
                    self._output_queue.put((True, return_message))
                # Player could not disprove the suggestion
                else:
                    disprove_character_str = PlayerEnum.to_string(disprove_character)
                    self._logger.debug('%s could not disprove the suggestion.', disprove_character_str)
                    
                    # Attempt to disprove suggestion with next suggester
                    self.perform_suggest()
                    
            # Handle accuse message
            elif message_enum == MessageEnum.ACCUSE and self.is_turn_character(player) == True:
                character = player.get_character()
                suspect = message_args[0]
                weapon = message_args[1]
                room = message_args[2]
                
                accussation = self._server_model.check_accusation(suspect, weapon, room)
                
                if accussation == True:
                    # Send an accuse message to all clients
                    response_args = [message_args, character, True]
                    return_message = Message(MessageEnum.ACCUSE, 1, response_args)
                    self._output_queue.put((True, return_message))
                else:
                    # if accusation is wrong set the players lost status to True
                    player.set_lost()
                    response_args = [message_args, character, False]
                    return_message = Message(MessageEnum.ACCUSE, 1, response_args)
                    self._output_queue.put((True, return_message))

            # Handle lobby ready and lobby unready messages
            elif message_enum == MessageEnum.LOBBY_READY or message_enum == MessageEnum.LOBBY_UNREADY:
                # Check to see if the game has already started
                game_started = self._server_model.is_game_started()
                
                if game_started == False:
                    # Set player ready status in player entry
                    ready_status = message_args[0]
                    self._logger.debug('Setting ready status for "%s" to %d.', player.get_name(), ready_status)
                    player.set_ready_status(ready_status)
                    
                    # Return player names and ready states
                    response_args = self._server_model.get_lobby_list()
                    return_message = Message(message_enum, 1, response_args)
                    
                    self._output_queue.put((True, return_message))
                    
                    # Check to see if the game is ready to start
                    if message_enum == MessageEnum.LOBBY_READY:
                        if self._server_model.is_game_ready() == True:
                            self._logger.debug('Starting game!')
                            
                            response_args = [PlayerEnum.MISS_SCARLET]
                            return_message = Message(MessageEnum.TURN_BEGIN, 1, response_args)
                            self._output_queue.put((True, return_message))
            
            elif message_enum == MessageEnum.TURN_OVER and self.is_turn_character(player) == True:
                # Send turn over message
                response_args = [player.get_character()]
                return_message = Message(MessageEnum.TURN_OVER, 1, response_args)
                self._output_queue.put((True, return_message))
                
                # Get the next turn player
                self._server_model.change_turn_character()
                next_character = self._server_model.get_turn_character()
                next_turn_player = self._server_model.get_player_from_character(next_character)

                # Skip players that have lost the game
                while player._has_lost == True:
                    self._logger.debug('Player: "%s" has lost the game. Their turn is skipped.', player.get_name())
                    self._server_model.change_turn_character()
                    next_character = self._server_model.get_turn_character()
                    next_turn_player = self._server_model.get_player_from_character(next_character)
                
                # Skip unconnected players turn
                while next_turn_player.is_connected() == False:
                    self._server_model.change_turn_character()
                    next_character = self._server_model.get_turn_character()
                    next_turn_player = self._server_model.get_player_from_character(next_character)
                
                # Send turn begin message
                response_args = [next_character]
                return_message = Message(MessageEnum.TURN_BEGIN, 1, response_args)
                self._output_queue.put((True, return_message))
    
    # Perform the suggest for players
    def perform_suggest(self):
        suggestion = self._server_model.get_suggestion()
        suspect = suggestion[0]
        weapon = suggestion[1]
        room = suggestion[2]
        
        disproven = False
        
        # Get the original suggester and next player to disprove
        suggester = self._server_model.get_suggester()
        disprove_character = self._server_model.get_next_suggest_character()
        disprove_player = self._server_model.get_player_from_character(disprove_character)
        
        # Attempt to disprove suggestion for all players that are not connected
        while disprove_player.is_connected() == False:
            disproven, matched_args = self._server_model.perform_suggest(disprove_player)
            
            if disproven == True:
                suspect = matched_args[0]
                weapon = matched_args[1]
                room = matched_args[2]
                
                response_args = [disprove_character, suspect, weapon, room]
                return_message = Message(MessageEnum.SUGGESTION_END, 1, response_args)
                
                self._output_queue.put((True, return_message))
                
                break
            else:
                disprove_character = self._server_model.get_next_suggest_character()
                disprove_player = self._server_model.get_player_from_character(disprove_character)
        
        # Check to see if an unconnected player disproved the suggestion
        if disproven == False:
            # All players have attempted to disprove suggestion
            if suggester == disprove_character:
                self._logger.debug('Suggestion could not be disproven by anyone.')
                
                response_args = [disprove_character, suspect, weapon, room]
                return_message = Message(MessageEnum.SUGGESTION_END, 1, response_args)
                self._output_queue.put((True, return_message))
            # Send suggest message to next disprover
            else:
                response_args = [suggester, disprove_character, suspect, weapon, room]
                return_message = Message(MessageEnum.SUGGEST, 1, response_args)
                self._output_queue.put((True, return_message))
    
    # Add a player using the specified address
    def add_player(self, address):
        self._server_model.add_player(address)
        
        # Send the player_enum chosen by the server back to the client
        player = self._server_model.get_player(address)
        
        character = player.get_character()
        player_enum_list = player.get_player_enum_list()
        weapon_enum_list = player.get_weapon_enum_list()
        room_enum_list = player.get_room_enum_list()
        
        # Send the card list to the player that connected
        response_args = [character, player_enum_list, weapon_enum_list, room_enum_list]
        return_message = Message(MessageEnum.LOBBY_CHANGE_PLAYER, 1, response_args)
        self._output_queue.put((False, return_message))
        
        # Send the player added to the lobby to all clients
        response_args = self._server_model.get_lobby_list()
        return_message = Message(MessageEnum.LOBBY_ADD, 1, response_args)
        self._output_queue.put((True, return_message))
    
    # Get the player associated with the specified address
    def get_player(self, address):
        return self._server_model.get_player(address)
    
    # Remove the player associated with the specified address
    def remove_player(self, address):
        self._server_model.remove_player(address)
    
    # Checks to see if the message is from the player whose turn it is
    def is_turn_character(self, player):
        character = player.get_character()
        turn_character = self._server_model.get_turn_character()
        
        if character == turn_character:
            return True
        else:
            self._logger.debug('Not this characters turn!')
            return False
