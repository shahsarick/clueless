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
            self._logger.debug('Received a move message.')
            
        elif message_enum == MessageEnum.SUGGEST:
            self._logger.debug('Received a suggest message.')
            
        elif message_enum == MessageEnum.ACCUSE:
            self._logger.debug('Received an accusation message.')
            
        elif message_enum == MessageEnum.LOBBY_ADD:
            player_name = message_args[0]
            
            self._logger.debug('Adding "%s" to lobby.', player_name)
            
            player.set_name(player_name)
            
            response_args = [player_name]
            return_message = Message(MessageEnum.LOBBY_ADD, 1, response_args)
            
            return (True, return_message)
            
        elif message_enum == MessageEnum.LOBBY_READY:
            self._logger.debug('Received a lobby ready message.')
            
        elif message_enum == MessageEnum.LOBBY_UNREADY:
            self._logger.debug('Received a lobby unready message.')
            
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
    
    def get_player(self, peername):
        return self._server_model.get_player(peername)
    
    def remove_player(self, peername):
        self._server_model.remove_player(peername)