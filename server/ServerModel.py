#!/usr/bin/env python

import logging

from common.Gameboard import Gameboard
from common.Player import Player
from common.PlayerEnum import PlayerEnum
from common.RoomEnum import RoomEnum
from common.WeaponEnum import WeaponEnum

class ServerModel:
    
    def __init__(self):
        self._logger = logging.getLogger('ServerModel')
        
        self._character_list = {PlayerEnum.MISS_SCARLET : False, \
                                PlayerEnum.COLONEL_MUSTARD : False, \
                                PlayerEnum.PROFESSOR_PLUM : False, \
                                PlayerEnum.MR_GREEN : False, \
                                PlayerEnum.MRS_WHITE : False, \
                                PlayerEnum.MRS_PEACOCK : False}
        self._player_list = []
        
        self._player_positions = {PlayerEnum.MISS_SCARLET : RoomEnum.HALLWAY_HALL_LOUNGE, \
                                  PlayerEnum.COLONEL_MUSTARD : RoomEnum.HALLWAY_LOUNGE_DINING_ROOM, \
                                  PlayerEnum.PROFESSOR_PLUM : RoomEnum.HALLWAY_LIBRARY_STUDY, \
                                  PlayerEnum.MR_GREEN : RoomEnum.HALLWAY_BALLROOM_CONSERVATORY, \
                                  PlayerEnum.MRS_WHITE : RoomEnum.HALLWAY_KITCHEN_BALLROOM, \
                                  PlayerEnum.MRS_PEACOCK : RoomEnum.HALLWAY_CONSERVATORY_LIBRARY}
        self._card_locations = {}
        self._weapon_locations = {WeaponEnum.CANDLESTICK : RoomEnum.STUDY, \
                                  WeaponEnum.ROPE : RoomEnum.BALLROOM, \
                                  WeaponEnum.LEAD_PIPE : RoomEnum.HALL, \
                                  WeaponEnum.REVOLVER : RoomEnum.BILLIARD_ROOM, \
                                  WeaponEnum.WRENCH : RoomEnum.CONSERVATORY, \
                                  WeaponEnum.KNIFE : RoomEnum.KITCHEN}
        
        self._gameboard = Gameboard()
        self._gameboard.setup_rooms()
        
        self._turn_order = []
    
    # Add a player to the player list using the given address
    def add_player(self, address):
        # Assign an available player_enum from the character list to the new player
        for player_enum in self._character_list:
            if self._character_list[player_enum] == False:
                self._character_list[player_enum] = True
                new_player = Player(address, player_enum)
                
                break
        
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
        
        # Check to see if the destination is a hallway
        if self._gameboard.is_hallway(destination_room) == True:
            # Check to see if a player is already in this hallway
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
    
    def get_player_position(self, player_enum):
        current_room = self._player_positions[player_enum]
        
        return current_room
            