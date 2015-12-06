#!/usr/bin/env python

import logging

from common.Message import Message
from common.MessageEnum import MessageEnum

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

class ServerMessage:

    def __init__(self):
        self._logger = logging.getLogger('ServerMessage')
    
    def handle_message(self, message):
        message_enum = message.get_message_enum()
        
        if message_enum == MessageEnum.MOVE:
            self._logger.debug('Received a move message.')
            
        elif message_enum == MessageEnum.SUGGEST:
            self._logger.debug('Received a suggest message.')
            
        elif message_enum == MessageEnum.ACCUSE:
            self._logger.debug('Received an accusation message.')
            
        elif message_enum == MessageEnum.LOBBY_ADD:
            self._logger.debug('Received a lobby add message.')
            
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