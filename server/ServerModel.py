#!/usr/bin/env python

import logging

from common.Player import Player
from common.PlayerEnum import PlayerEnum

class ServerModel:
    
    def __init__(self):
        self._logger = logging.getLogger('ServerModel')
        
        self._character_list = [[PlayerEnum.MISS_SCARLET, False], \
                                [PlayerEnum.COLONEL_MUSTARD, False], \
                                [PlayerEnum.PROFESSOR_PLUM, False], \
                                [PlayerEnum.MR_GREEN, False], \
                                [PlayerEnum.MRS_WHITE, False], \
                                [PlayerEnum.MRS_PEACOCK, False]]
        self._player_list = []
        
        self._player_positions = []
        self._card_locations = []
        self._weapon_locations = []
        
        self._turn_order = []
    
    # Add a player to the player list using the given address
    def add_player(self, address):
        # Assign an available player_enum from the character list to the new player
        for i in range(len(self._character_list)):
            player_enum = self._character_list[i][0]
            chosen = self._character_list[i][1]
            
            if chosen == False:
                self._character_list[i][1] = True
                new_player = Player(address, player_enum)
                
                break
        
        self._logger.debug('Adding (%s, %s) as player_enum %s to player list.', address[0], address[1], new_player.get_player_enum())
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
                
                for i in range(len(self._character_list)):
                    if player_enum == self._character_list[i][0]:
                        self._character_list[i][1] = False
                        
                        break
                
                # Remove the player from the player list
                self._player_list.remove(player)
                
                break
    
    # Compare the address to determine if they are equal
    def compare_addresses(self, address1, address2):
        if address1[0] == address2[0] and address1[1] == address2[1]:
            return True
        else:
            return False
    
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
            