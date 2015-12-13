#!/usr/bin/env python

import logging
from random import randint

from common.Gameboard import Gameboard
from common.Player import Player
from common.PlayerEnum import PlayerEnum
from common.RoomEnum import RoomEnum
from common.TurnEnum import TurnEnum
from common.WeaponEnum import WeaponEnum

class ServerModel:
    
    def __init__(self):
        self._logger = logging.getLogger('ServerModel')
        
        # Create character dictionary and player list for lobby and socket use
        self._character_list = {PlayerEnum.MISS_SCARLET : False, \
                                PlayerEnum.COLONEL_MUSTARD : False, \
                                PlayerEnum.PROFESSOR_PLUM : False, \
                                PlayerEnum.MR_GREEN : False, \
                                PlayerEnum.MRS_WHITE : False, \
                                PlayerEnum.MRS_PEACOCK : False}
        self._player_list = []
        
        # Set card locations
        self._player_positions = {PlayerEnum.MISS_SCARLET : RoomEnum.HALLWAY_HALL_LOUNGE, \
                                  PlayerEnum.COLONEL_MUSTARD : RoomEnum.HALLWAY_LOUNGE_DINING_ROOM, \
                                  PlayerEnum.PROFESSOR_PLUM : RoomEnum.HALLWAY_LIBRARY_STUDY, \
                                  PlayerEnum.MR_GREEN : RoomEnum.HALLWAY_BALLROOM_CONSERVATORY, \
                                  PlayerEnum.MRS_WHITE : RoomEnum.HALLWAY_KITCHEN_BALLROOM, \
                                  PlayerEnum.MRS_PEACOCK : RoomEnum.HALLWAY_CONSERVATORY_LIBRARY}
        
        self._weapon_locations = {WeaponEnum.CANDLESTICK : RoomEnum.STUDY, \
                                  WeaponEnum.ROPE : RoomEnum.BALLROOM, \
                                  WeaponEnum.LEAD_PIPE : RoomEnum.HALL, \
                                  WeaponEnum.REVOLVER : RoomEnum.BILLIARD_ROOM, \
                                  WeaponEnum.WRENCH : RoomEnum.CONSERVATORY, \
                                  WeaponEnum.KNIFE : RoomEnum.KITCHEN}
        
        # Set turn order
        self._turn_order = [PlayerEnum.MISS_SCARLET, 
                            PlayerEnum.COLONEL_MUSTARD, 
                            PlayerEnum.MRS_WHITE, 
                            PlayerEnum.MR_GREEN, 
                            PlayerEnum.MRS_PEACOCK, 
                            PlayerEnum.PROFESSOR_PLUM]
        self._turn_state = TurnEnum.MOVE
        
        # Create gameboard
        self._gameboard = Gameboard()
        self._gameboard.setup_rooms()
        
        # Fill envelope with suspect, weapon, and room
        suspect = randint(1, 6)
        weapon = randint(1, 6)
        room = randint(1, 9)
        
        self._envelope = [suspect, weapon, room]
        
        self._game_started = False

        # set whos turn it is initially by array index of self._turn_order
        self.currentTurn = 0

    # returns the player whos turn it is
    def getCurrentTurn(self):
        return self._turn_order[self.currentTurn]
    # increases the turn pointer
    def updateTurn(self):
        if self.currentTurn <= 4:
            self.currentTurn = self.currentTurn + 1
        else:
            self.currentTurn = 0


    # Add a player to the player list using the given address
    def add_player(self, address):
        # Assign an available player_enum from the character list to the new player
        for player_enum in self._character_list:
            if self._character_list[player_enum] == False:
                self._character_list[player_enum] = True
                new_player = Player(address, player_enum)
                
                break
        
        # Add the new player to the player list
        player_enum = new_player.get_player_enum()
        player_enum_str = PlayerEnum.to_string(player_enum)
        
        self._logger.debug('Adding (%s, %s) as %s to player list.', address[0], address[1], player_enum_str)
        self._player_list.append(new_player)
    
    # Get the player with the associated address
    def get_player(self, address):
        self._logger.debug('Retrieving player mapped to (%s, %s).' % address)
        
        for player in self._player_list:
            player_address = player.get_address()
            
            if self.compare_addresses(address, player_address) == True:
                return player
    
    # Remove the player from the game and free the associated player_enum in the character list
    def remove_player(self, address):
        self._logger.debug('Removing (%s, %s) from player list.' % address)
        
        for player in self._player_list:
            player_address = player.get_address()
            
            if self.compare_addresses(address, player_address) == True:
                # Make the player_enum in the character list available to be used by someone else
                player_enum = player.get_player_enum()
                self._character_list[player_enum] = False
                
                # Remove the player from the player list
                self._player_list.remove(player)
                
                break
    
    # Compare the address to determine if they are equal
    def compare_addresses(self, address1, address2):
        if address1[0] == address2[0] and address1[1] == address2[1]:
            return True
        else:
            return False
    
    # Attempt to move the player to the destination room
    def perform_move(self, player_enum, destination_room):
        current_room = self._player_positions[player_enum]
        
        player_enum_str = PlayerEnum.to_string(player_enum)
        current_room_str = RoomEnum.to_string(current_room)
        destination_room_str = RoomEnum.to_string(destination_room)
        self._logger.debug('Attempting to move %s from "%s" to "%s".', player_enum_str, current_room_str, destination_room_str)
        
        # Check to see if the move is valid on the gameboard
        valid_move = self._gameboard.is_valid_move(current_room, destination_room)
        
        # Check to see if the destination is an occupied hallway
        if self._gameboard.is_hallway(destination_room) == True:
            for player_position, player_location in self._player_positions.items():
                if destination_room == player_location:
                    valid_move = False
                    
                    break
        
        # Update the player position if the move is valid
        if valid_move == True:
            self._player_positions[player_enum] = destination_room
        
        return valid_move
    
    # Get the list of players in the lobby and their associated ready status
    def get_lobby_list(self):
        self._logger.debug('Retrieving lobby list:')
        
        lobby_list = []
        
        for player in self._player_list:
            player_name = player.get_name()
            ready_state = player.get_ready_status()
            self._logger.debug('\t(%s, %s)', player_name, ready_state)
            
            lobby_entry = [player_name, ready_state]
            lobby_list.append(lobby_entry)
        
        return lobby_list
    
    # Get the position for the specified player_enum
    def get_player_position(self, player_enum):
        current_room = self._player_positions[player_enum]
        
        return current_room
    
    # Check to see if the game is ready to start
    def is_game_ready(self):
        self._logger.debug('Checking to see if the game is ready to start.')
        
        # Check to make sure the minimum number of players are in the game
        if len(self._player_list) < 2:
            return False
        
        # Check to see if everyone in the game is ready
        for player in self._player_list:
            if player.get_ready_status() == False:
                return False
        
        self._game_started = True
        
        return True
    
    # Check to see if the game has started
    def is_game_started(self):
        return self._game_started
            