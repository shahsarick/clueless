#!/usr/bin/env python

import cPickle as pickle
import logging
import SocketServer

from common.Message import Message
from common.MessageEnum import MessageEnum

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

class ServerMessage(SocketServer.BaseRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ServerMessage')
        self.logger.debug('__init__')
        
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        
        return
    
    def setup(self):
        self.logger.debug('setup')
        
        return SocketServer.BaseRequestHandler.setup(self)
    
    def handle(self):
        self.logger.debug('handle')
        
        # Read the message sent by the client
        data_string = self.request.recv(1024)
        message = pickle.loads(data_string)
        
        message_enum = message.message_enum
        
        if message_enum == MessageEnum.MOVE:
            self.logger.debug('Received a move message.')
            
        elif message_enum == MessageEnum.SUGGEST:
            self.logger.debug('Received a suggest message.')
            
        elif message_enum == MessageEnum.ACCUSE:
            self.logger.debug('Received an accusation message.')
            
        elif message_enum == MessageEnum.LOBBY_ADD:
            self.logger.debug('Received a lobby add message.')
            
        elif message_enum == MessageEnum.LOBBY_READY:
            self.logger.debug('Received a lobby ready message.')
            
        elif message_enum == MessageEnum.LOBBY_UNREADY:
            self.logger.debug('Received a lobby unready message.')
            
        elif message_enum == MessageEnum.LOBBY_CHANGE_PLAYER:
            self.logger.debug('Received a lobby change player message.')
            
        elif message_enum == MessageEnum.GAME_STATE_CHANGE:
            self.logger.debug('Received a game state change message.')
            
        elif message_enum == MessageEnum.TURN_OVER:
            self.logger.debug('Received a turn over message.')
            
        elif message_enum == MessageEnum.TURN_BEGIN:
            self.logger.debug('Received a turn begin message.')
            
        elif message_enum == MessageEnum.ERROR:
            self.logger.debug('Received an error message.')
            
        self.logger.debug('Message contents: "%s, %s, %s"' % message.get_message_contents())
        
        # Send a message back to the client
        message = Message(MessageEnum.TURN_OVER, 1, "Your turn is over!!")
        data_string = pickle.dumps(message)
        self.request.sendall(data_string)
        
        return
    
    def finish(self):
        self.logger.debug('finish')
        
        return SocketServer.BaseRequestHandler.finish(self)