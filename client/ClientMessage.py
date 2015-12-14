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
    
    # Returns the reference to the client model instance
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
            #num_args = message.get_num_args()
            message_args = message.get_args()
            
            # Handle move message
            if message_enum == MessageEnum.MOVE:
                valid_move = message_args[0]
                
                if valid_move == True:
                    character = message_args[1]
                    old_room = message_args[2]
                    new_room = message_args[3]
                    
                    old_room_str = RoomEnum.to_string(old_room)
                    character_str = PlayerEnum.to_string(character)
                    
                    new_room_str = RoomEnum.to_string(new_room)
                    self._logger.debug('%s moved from "%s" to "%s".', character_str, old_room_str, new_room_str)
                    
                    # Move the player to the specified room
                    self._client_model.move_character(character, new_room)
                    
                    # Get suggestion status
                    must_suggest = self._client_model.get_suggest_status()
                    
                    if must_suggest == True:
                        self._logger.debug('You need to make a suggestion!')
                        
                        #TODO: Notify the player to make a suggestion by signaling the GUI
                    else:
                        if self._client_model.get_character() == character:
                            self._logger.debug('You must now make an accusation or end your turn.')
                else:
                    self._logger.debug('Invalid move!')
            
            # Handle suggest message
            elif message_enum == MessageEnum.SUGGEST:
                character = message_args[0]
                disprove_character = message_args[1]
                
                suspect = message_args[2]
                weapon = message_args[3]
                room = message_args[4]
                
                character_str = PlayerEnum.to_string(character)
                disprover_character_str = PlayerEnum.to_string(disprove_character)
                
                suspect_str = PlayerEnum.to_string(suspect)
                weapon_str = WeaponEnum.to_string(weapon)
                room_str = RoomEnum.to_string(room)
                
                self._logger.debug('%s has made the following suggestion: (%s, %s, %s)', character_str, suspect_str, weapon_str, room_str)
                self._logger.debug('%s is now attempting to disprove the suggestion.', disprover_character_str)
                
                # Set the suggestion in the client model
                suggestion = [suspect, weapon, room]
                self._client_model.set_suggestion(suggestion)
                
                # Check to see if this player needs to attempt to disprove the suggestion
                if disprove_character == self._client_model.get_character():
                    self._logger.debug('You must now try to disprove the suggestion!')
                    
                    #TODO: Notify the player to disprove the suggestion by signaling the GUI
            
            # Handle suggest end message
            elif message_enum == MessageEnum.SUGGESTION_END:
                self._logger.debug('Suggestion turn has ended.')
                
                character = message_args[0]
                player_enum = message_args[1]
                weapon = message_args[2]
                room = message_args[3]
                
                character_str = PlayerEnum.to_string(character)
                
                # This player made the original suggestion
                if self._client_model.has_suggested() == True:
                    if player_enum is not None:
                        player_enum_str = PlayerEnum.to_string(player_enum)
                        self._logger.debug('%s disproved you with the %s card.', character_str, player_enum_str)
                    elif weapon is not None:
                        weapon_str = WeaponEnum.to_string(weapon)
                        self._logger.debug('%s disproved you with the %s card.', character_str, weapon_str)
                    elif room is not None:
                        room_str = RoomEnum.to_string(room)
                        self._logger.debug('%s disproved you with the %s card.', character_str, room_str)
                    else:
                        self._logger.debug('No one disproved your suggestion!')
                    
                    self._logger.debug('You must now make an accusation or end your turn.')
                    
                    #TODO: Notify the player to make an accusation by signaling the GUI
                else:
                    self._logger.debug('%s disproved the suggestion!', character_str)
            
            # Handle accuse message
            elif message_enum == MessageEnum.ACCUSE:
                self._logger.debug('Received an accusation message.')
                accusation = message_args[0]
                character = message_args[1]
                correct = message_args[2]

                character_str = PlayerEnum.to_string(self._client_model.get_character())
                suspect_str = PlayerEnum.to_string(accusation[0])
                weapon_str = WeaponEnum.to_string(accusation[1])
                room_str = RoomEnum.to_string(accusation[2])
                self._logger.debug('%s has made the following accusation: (%s, %s, %s)', character_str, suspect_str, weapon_str, room_str)

                if correct == True:
                    self._logger.debug('This player was correct and has won the game!')
                    self._client_model.set_accuse_status(True)
                    
                    self._client_model.set_won_game(True)
                    
                    #TODO: Notify the player that they have won by signaling the GUI
                else:
                    self._logger.debug('This accusation was false! This player has lost the game!')
                    self._client_model.set_accuse_status(True)
                    
                    self._client_model.set_won_game(False)
                    
                    #TODO: Notify the player that they have lost by signaling the GUI
            
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
                
                #TODO: Notify the player that the lobby has been updated by signaling the GUI
            
            # Handle lobby change player message
            elif message_enum == MessageEnum.LOBBY_CHANGE_PLAYER:
                character = message_args[0]
                player_enum_list = message_args[1]
                weapon_enum_list = message_args[2]
                room_enum_list = message_args[3]
                
                self._client_model.set_character(character)
                self._client_model.set_player_enum_list(player_enum_list)
                self._client_model.set_weapon_enum_list(weapon_enum_list)
                self._client_model.set_room_enum_list(room_enum_list)
                
                character_str = PlayerEnum.to_string(character)
                player_enum_list_str = ", ".join(PlayerEnum.to_string(pe) for pe in player_enum_list)
                weapon_enum_list_str = ", ".join(WeaponEnum.to_string(we) for we in weapon_enum_list)
                room_enum_list_str = ", ".join(RoomEnum.to_string(re) for re in room_enum_list)
                
                self._logger.debug('You have been assigned the character %s and the following cards:.', character_str)
                self._logger.debug('Player enum list: %s', player_enum_list_str)
                self._logger.debug('Weapon enum list: %s', weapon_enum_list_str)
                self._logger.debug('Room enum list: %s', room_enum_list_str)
                
                #TODO: Notify the player of which character they are and what cards they have by signaling the GUI
            # Handle turn over message
            elif message_enum == MessageEnum.TURN_OVER:
                character = message_args[0]
                
                self._logger.debug('It is no longer "%s\'s" turn!.', PlayerEnum.to_string(character))
                
                # Reset move variables for turn player
                if character == self._client_model.get_character():
                    self._client_model.reset_all()
                
                #TODO: Notify the player that the specified character's turn is over by signaling the GUI
            # Handle turn begin message
            elif message_enum == MessageEnum.TURN_BEGIN:
                character = message_args[0]
                
                self._logger.debug('It is now "%s\'s" turn!.', PlayerEnum.to_string(character))
                
                if character == self._client_model.get_character():
                    self._logger.debug('It is now your turn!')
                
                    #TODO: Notify the player that it is their turn by signaling the GUI
    
    # Checks to see if a suggestion must be made
    def need_suggestion(self):
        return self._client_model.get_suggest_status()
    
    # Makes a suggestion
    def make_suggestion(self):
        self._client_model.make_suggestion()
    
    # Gets the suggestion made
    def get_suggestion(self):
        return self._client_model.get_suggestion()
    
    # Get the list of cards owned by this client
    def get_cards(self):
        return self._client_model.get_cards()