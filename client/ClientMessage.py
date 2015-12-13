#!/usr/bin/env python

import cPickle as pickle
import logging
import Queue
import threading

from client.Client import Client
from client.ClientModel import ClientModel
from common.Gameboard import Gameboard
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
        self._client_model = ClientModel()
        self._gameboard = Gameboard()
    # Connects to the server
    def connect_to_server(self, host, port):
        #TODO: May need to move connect_to_server into worker thread to prevent server messages coming back before we're ready for them
        connected = self._client.connect_to_server(host, port)
        
        if connected == True:
            self.start_client()
            
            return True
        else:
            return False
    def return_client_model_instance(self):
        return self._client_model
    # Starts the client communication thread
    def start_client(self):
        self._logger.debug('Starting client communication thread.')
        
        client_thread = threading.Thread(target=self._client.run)
        client_thread.start()
    
    # Send a message to the server
    def send_message(self, message):
        self._input_queue.put(message)
    
    # Handle the messages sent by the server
    def handle_message(self):
        while self._output_queue.qsize() > 0:
            message = self._output_queue.get()
            
            message_enum = message.get_message_enum()
            num_args = message.get_num_args()
            message_args = message.get_args()
            
            # Handle move messages
            if message_enum == MessageEnum.MOVE:
                valid_move = message_args[0]
                
                if valid_move == True:
                    player_enum = message_args[1]
                    old_room = message_args[2]
                    new_room = message_args[3]
                    
                    old_room_str = RoomEnum.to_string(old_room)
                    player_enum_str = PlayerEnum.to_string(player_enum)

                    # update the in-room status of the client
                    if self._gameboard.is_hallway(new_room)==True:
                        self._client_model.moved_to_room(False)
                        self._client_model.has_moved = True
                    if self._gameboard.is_hallway(new_room)==False:
                        self._client_model.has_moved = True
                        self._client_model.must_suggest = True
                        #TODO: update the GUI to notify user to make a suggestion


                    new_room_str = RoomEnum.to_string(new_room)
                    self._logger.debug('%s moved from "%s" to "%s".', player_enum_str, old_room_str, new_room_str)
                else:
                    self._logger.debug('Invalid move!')
            
            # Handle suggest messages
            elif message_enum == MessageEnum.SUGGEST:
                self._logger.debug('Received a suggest message.')
            
            # Handle accuse message
            elif message_enum == MessageEnum.ACCUSE:
                self._logger.debug('Received an accusation message.')
            
            # Handle lobby ready and unready messages
            elif message_enum == MessageEnum.LOBBY_ADD or message_enum == MessageEnum.LOBBY_READY or message_enum == MessageEnum.LOBBY_UNREADY:
                # Refresh the lobby with the updated list of player names and ready states
                # This keeps the lobby in sync in case someone leaves and provides the entire lobby list to new players
                lobby_list = message_args
                
                self._logger.debug('Printing lobby list:')
                
                for lobby_entry in lobby_list:
                    player_name = lobby_entry[0]
                    ready_state = lobby_entry[1]
                    
                    self._logger.debug('\t(%s, %s).', player_name, ready_state)
            
            # Handle lobby change player message
            elif message_enum == MessageEnum.LOBBY_CHANGE_PLAYER:
                player_enum = message_args[0]
                
                self._logger.debug('You have been assigned the character "%s".', PlayerEnum.to_string(player_enum))
                
                self._client_model.set_player_enum(player_enum)
            
            # Handle game state change message
            elif message_enum == MessageEnum.GAME_STATE_CHANGE:
                self._logger.debug('Received a game state change message.')
            
            # Handle turn over message
            elif message_enum == MessageEnum.TURN_OVER:
                self._logger.debug('Received a turn over message.')
            
            # Handle turn begin message
            elif message_enum == MessageEnum.TURN_BEGIN:
                player_enum = message_args[0]
                
                self._logger.debug('It is now "%s\'s" turn!.', PlayerEnum.to_string(player_enum))
                
                if player_enum == self._client_model.get_player_enum():
                    self._logger.debug('It is now your turn!')
            
            # Handle error message
            elif message_enum == MessageEnum.ERROR:
                self._logger.debug('Received an error message.')
