#!/usr/bin/env python

import cPickle as pickle
import logging
import Queue
import threading

from client.Client import Client

from common.Message import Message
from common.MessageEnum import MessageEnum

class ClientMessage:
    
    def __init__(self):
        self._logger = logging.getLogger('ClientMessage')
        
        self._input_queue = Queue.Queue()
        self._output_queue = Queue.Queue()

        self.i = 0
        
        self._client = Client(self._input_queue, self._output_queue)
    
    def connect_to_server(self, host, port):
        connected = self._client.connect_to_server(host, port)
        
        if connected == True:
            self.start_client()
            
            return True
        else:
            return False
    
    def start_client(self):
        self._logger.debug('Starting client communication thread.')
        
        client_thread = threading.Thread(target=self._client.run)
        client_thread.start()
    
    def send_message(self, message):
        self._logger.debug('Sending data: "%s, %s, %s"' % message.get_message_contents())
        
        # Send message to server
        data_string = pickle.dumps(message)
        self._input_queue.put(data_string)
    
    def handle_message(self):
        data_string = self._output_queue.get()
        message = pickle.loads(data_string)
        
        self._logger.debug('Message from server: "%s, %s, %s"' % message.get_message_contents())
        
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