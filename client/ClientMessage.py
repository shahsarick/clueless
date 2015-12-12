#!/usr/bin/env python

import cPickle as pickle
import logging
import Queue
import threading

from client.Client import Client

from common.MessageEnum import MessageEnum
from common.PlayerEnum import PlayerEnum
from common.RoomEnum import RoomEnum

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
        # Send message to server
        data_string = pickle.dumps(message)
        self._input_queue.put(data_string)
    
    def handle_message(self):
        data_string = self._output_queue.get()
        message = pickle.loads(data_string)
        
        message_enum = message.get_message_enum()
        num_args = message.get_num_args()
        message_args = message.get_args()
        
        if message_enum == MessageEnum.MOVE:
            if len(message_args) > 1:
                old_room = message_args[0]
                player_enum = message_args[1]
                new_room = message_args[2]
                
                old_room_str = RoomEnum.to_string(old_room)
                player_enum_str = PlayerEnum.to_string(player_enum)
                new_room_str = RoomEnum.to_string(new_room)
                self._logger.debug('%s moved from "%s" to "%s".', player_enum_str, old_room_str, new_room_str)
            else:
                self._logger.debug('Invalid move!')
            
        elif message_enum == MessageEnum.SUGGEST:
            self._logger.debug('Received a suggest message.')
            
        elif message_enum == MessageEnum.ACCUSE:
            self._logger.debug('Received an accusation message.')
        
        # Refresh the lobby with the updated list of player names and ready states
        # This keeps the lobby in sync in case someone leaves and provides the entire lobby list to new players
        elif message_enum == MessageEnum.LOBBY_ADD or message_enum == MessageEnum.LOBBY_READY or message_enum == MessageEnum.LOBBY_UNREADY:
            lobby_list = message_args
            
            self._logger.debug('Printing lobby list:')
            
            for lobby_entry in lobby_list:
                player_name = lobby_entry[0]
                ready_state = lobby_entry[1]
                
                self._logger.debug('\t(%s, %s).', player_name, ready_state)
        
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