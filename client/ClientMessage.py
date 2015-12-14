#!/usr/bin/env python

import logging
import Queue
import threading

from client.Client import Client
from client.ClientModel import ClientModel
from common.MessageEnum import MessageEnum
from common.PlayerEnum import PlayerEnum
from common.RoomEnum import RoomEnum
from common.WeaponEnum import WeaponEnum

class ClientMessage:
    
    def __init__(self):
        self._logger = logging.getLogger('ClientMessage')
        
        self._input_queue = Queue.Queue()
        self._output_queue = Queue.Queue()

        self.i = 0
        
        self._client = Client(self._input_queue, self._output_queue)
        self._client_model = ClientModel()
    
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
                    
                    new_room_str = RoomEnum.to_string(new_room)
                    self._logger.debug('%s moved from "%s" to "%s".', player_enum_str, old_room_str, new_room_str)
                    
                    # Move the player to the specified room
                    self._client_model.move_player(player_enum, new_room)
                    
                    # Get suggestion status
                    must_suggest = self._client_model.get_suggest_status()
                    
                    if must_suggest == True:
                        self._logger.debug('You need to make a suggestion!')
                        
                        #TODO: Notify the player to make a suggestion by signaling the GUI
                else:
                    self._logger.debug('Invalid move!')
            
            # Handle suggest messages
            elif message_enum == MessageEnum.SUGGEST:
                player_enum = message_args[0]
                suggest_player_enum = message_args[1]
                suspect = message_args[2]
                weapon = message_args[3]
                room = message_args[4]
                
                player_enum_str = PlayerEnum.to_string(player_enum)
                suggest_player_enum_str = PlayerEnum.to_string(suggest_player_enum)
                suspect_str = PlayerEnum.to_string(suspect)
                weapon_str = WeaponEnum.to_string(weapon)
                room_str = RoomEnum.to_string(room)
                
                self._logger.debug('%s has made the following suggestion: (%s, %s, %s)', player_enum_str, suspect_str, weapon_str, room_str)
                self._logger.debug('%s is now attempting to disprove the suggestion.', suggest_player_enum_str)
                
                # Set the suggestion in the client model
                suggestion = [suspect, weapon, room]
                self._client_model.set_suggestion(suggestion)
                
                # Check to see if this player needs to attempt to disprove the suggestion
                if suggest_player_enum == self._client_model.get_player_enum():
                    self._logger.debug('You must now try to disprove the suggestion!')
                    
                    #TODO: Notify the player to disprove the suggestion by signaling the GUI
                    
                    pass
            # Handle accuse message
            elif message_enum == MessageEnum.ACCUSE:
                self._logger.debug('Received an accusation message.')
                accusation = message_args[0]
                player_enum = message_args[1]
                correct = message_args[2]

                player_enum_str = PlayerEnum.to_string(player_enum)
                suspect_str = PlayerEnum.to_string(accusation[0])
                weapon_str = WeaponEnum.to_string(accusation[1])
                room_str = RoomEnum.to_string(accusation[2])
                self._logger.debug('%s has made the following accusation: (%s, %s, %s)', player_enum_str, suspect_str, weapon_str, room_str)

                if correct == True:
                    self._logger.debug('This player was correct and has won the game!')
                    self._client_model.set_accuse_status(True)
                    #TODO: end the game when a player makes a correct accusation
                else:
                    self._logger.debug('This accusation was false! This player has lost the game!')
                    self._client_model.set_accuse_status(True)
            
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
                weapon_enum = message_args[1]
                room_enum = message_args[2]
                
                self._client_model.set_player_enum(player_enum)
                self._client_model.set_weapon_enum(weapon_enum)
                self._client_model.set_room_enum(room_enum)
                
                player_enum_str = PlayerEnum.to_string(player_enum)
                weapon_enum_str = WeaponEnum.to_string(weapon_enum)
                room_enum_str = RoomEnum.to_string(room_enum)
                
                self._logger.debug('You have been assigned the cards: (%s, %s, %s).', player_enum_str, weapon_enum_str, room_enum_str)
            
            # Handle turn over message
            elif message_enum == MessageEnum.TURN_OVER:
                self._logger.debug('Received a turn over message.')
                
                #TODO: Set player turn over (reset client_model info)
            
            # Handle turn begin message
            elif message_enum == MessageEnum.TURN_BEGIN:
                player_enum = message_args[0]
                
                self._logger.debug('It is now "%s\'s" turn!.', PlayerEnum.to_string(player_enum))
                
                if player_enum == self._client_model.get_player_enum():
                    self._logger.debug('It is now your turn!')
    
    def need_suggestion(self):
        return self._client_model.get_suggest_status()
    
    def make_suggestion(self):
        self._client_model.make_suggestion()