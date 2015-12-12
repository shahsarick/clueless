#!/usr/bin/env python

import logging

from common.Message import Message
from common.MessageEnum import MessageEnum

from server.ServerModel import ServerModel

class ServerMessage:

    def __init__(self):
        self._logger = logging.getLogger('ServerMessage')
        
        self._server_model = ServerModel()
    
    def handle_message(self, message, player):
        message_enum = message.get_message_enum()
        message_args = message.get_args()
        
        if message_enum == MessageEnum.MOVE:
            player_enum = player.get_player_enum()
            current_room = self._server_model.get_player_position(player_enum)
            destination_room = message_args[0]
            
            valid_move = self._server_model.perform_move(player_enum, destination_room)
            
            broadcast = True
            
            if valid_move == True:
                new_room = self._server_model.get_player_position(player_enum)
                response_args = [True, player_enum, current_room, new_room]
            else:
                response_args = [False]
                broadcast = False
            
            return_message = Message(MessageEnum.MOVE, 1, response_args)
            
            return (broadcast, return_message)
            
        elif message_enum == MessageEnum.SUGGEST:
            self._logger.debug('Received a suggest message.')
            
        elif message_enum == MessageEnum.ACCUSE:
            self._logger.debug('Received an accusation message.')
            
        elif message_enum == MessageEnum.LOBBY_ADD:
            # Set player name in player entry
            player_name = message_args[0]
            self._logger.debug('Adding "%s" to lobby.', player_name)
            player.set_name(player_name)
            
            # Return player names and ready states
            response_args = self._server_model.get_lobby_list()
            return_message = Message(MessageEnum.LOBBY_ADD, 1, response_args)
            
            return (True, return_message)
            
        elif message_enum == MessageEnum.LOBBY_READY or message_enum == MessageEnum.LOBBY_UNREADY:
            # Set player ready status in player entry
            ready_status = message_args[0]
            self._logger.debug('Setting ready status for "%s" to %d.', player.get_name(), ready_status)
            player.set_ready_status(ready_status)
            
            # Return player names and ready states
            response_args = self._server_model.get_lobby_list()
            return_message = Message(message_enum, 1, response_args)
                        
            return (True, return_message)
            
        elif message_enum == MessageEnum.LOBBY_CHANGE_PLAYER:
            self._logger.debug('Received a lobby change player message.')
            
        elif message_enum == MessageEnum.GAME_STATE_CHANGE:
            self._logger.debug('Received a game state change message.')
            
        elif message_enum == MessageEnum.TURN_OVER:
            self._logger.debug('Received a turn over message.')
            
        elif message_enum == MessageEnum.TURN_BEGIN:
            self._logger.debug('Received a turn begin message.')
            
        elif message_enum == MessageEnum.ERROR:
            self._logger.debug('Received an error message.')
    
    def add_player(self, address):
        self._server_model.add_player(address)
    
    def get_player(self, address):
        return self._server_model.get_player(address)
    
    def remove_player(self, address):
        self._server_model.remove_player(address)