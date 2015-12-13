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
            message_args = message.get_args()
            
            # Handle move message
            if message_enum == MessageEnum.MOVE & self.checkValidTurn(player):
                player_enum = player.get_player_enum()
                current_room = self._server_model.get_player_position(player_enum)
                destination_room = message_args[0]
                
                valid_move = self._server_model.perform_move(player_enum, destination_room)
                
                if valid_move == True:
                    new_room = self._server_model.get_player_position(player_enum)
                    response_args = [True, player_enum, current_room, new_room]
                    broadcast = True
                else:
                    response_args = [False]
                    broadcast = False
                
                return_message = Message(MessageEnum.MOVE, 1, response_args)
                
                self._output_queue.put((broadcast, return_message))
                # update the turn_state if necessary

            # Handle suggest message
            elif message_enum == MessageEnum.SUGGEST:
                self._logger.debug('Received a suggest message.')
            
            # Handle accuse message
            elif message_enum == MessageEnum.ACCUSE:
                self._logger.debug('Received an accusation message.')
            
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

            elif message_enum == MessageEnum.TURN_OVER & self.checkValidTurn(player):
                print "something"
                self._server_model.updateTurn()

    # Add a player using the specified address
    def add_player(self, address):
        self._server_model.add_player(address)
        
        # Send the player_enum chosen by the server back to the client
        player = self._server_model.get_player(address)
        player_enum = player.get_player_enum()
        
        response_args = [player_enum]
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

    def checkValidTurn(self,player):
        thisPlayer = self._server_model.getCurrentTurn()
        if player._player_enum == thisPlayer:
            return True
        else:
            self._logger.debug('Not this players turn!')
            return False
