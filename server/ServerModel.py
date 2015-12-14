#!/usr/bin/env python

import logging
from random import randint

from common.Gameboard import Gameboard
from common.Player import Player
from common.PlayerEnum import PlayerEnum
from common.RoomEnum import RoomEnum
from common.WeaponEnum import WeaponEnum

class ServerModel:
    
    def __init__(self):
        self._logger = logging.getLogger('ServerModel')
        
        # Create character dictionary and player list for lobby and socket use
        self._character_list = {PlayerEnum.MISS_SCARLET : False, 
                                PlayerEnum.COLONEL_MUSTARD : False, 
                                PlayerEnum.MRS_WHITE : False, 
                                PlayerEnum.MR_GREEN : False, 
                                PlayerEnum.MRS_PEACOCK : False, 
                                PlayerEnum.PROFESSOR_PLUM : False}
        
        self._player_enum_list = {PlayerEnum.MISS_SCARLET : False, 
                                  PlayerEnum.COLONEL_MUSTARD : False, 
                                  PlayerEnum.MRS_WHITE : False, 
                                  PlayerEnum.MR_GREEN : False, 
                                  PlayerEnum.MRS_PEACOCK : False, 
                                  PlayerEnum.PROFESSOR_PLUM : False}
        
        self._weapon_enum_list = {WeaponEnum.CANDLESTICK : False, 
                                  WeaponEnum.ROPE : False,
                                  WeaponEnum.LEAD_PIPE : False,
                                  WeaponEnum.REVOLVER : False,
                                  WeaponEnum.WRENCH : False,
                                  WeaponEnum.KNIFE : False}
        
        self._room_enum_list = {RoomEnum.STUDY : False, 
                                RoomEnum.HALL : False, 
                                RoomEnum.LOUNGE : False, 
                                RoomEnum.DINING_ROOM : False, 
                                RoomEnum.KITCHEN : False, 
                                RoomEnum.BALLROOM : False, 
                                RoomEnum.CONSERVATORY : False, 
                                RoomEnum.LIBRARY : False, 
                                RoomEnum.BILLIARD_ROOM : False}
        
        self._player_list = []
        
        # Set card locations
        self._character_positions = {PlayerEnum.MISS_SCARLET : RoomEnum.HALLWAY_HALL_LOUNGE,
                                     PlayerEnum.COLONEL_MUSTARD : RoomEnum.HALLWAY_LOUNGE_DINING_ROOM,
                                     PlayerEnum.PROFESSOR_PLUM : RoomEnum.HALLWAY_LIBRARY_STUDY,
                                     PlayerEnum.MR_GREEN : RoomEnum.HALLWAY_BALLROOM_CONSERVATORY,
                                     PlayerEnum.MRS_WHITE : RoomEnum.HALLWAY_KITCHEN_BALLROOM,
                                     PlayerEnum.MRS_PEACOCK : RoomEnum.HALLWAY_CONSERVATORY_LIBRARY}
        
        self._weapon_locations = {WeaponEnum.CANDLESTICK : RoomEnum.STUDY, 
                                  WeaponEnum.ROPE : RoomEnum.BALLROOM, 
                                  WeaponEnum.LEAD_PIPE : RoomEnum.HALL, 
                                  WeaponEnum.REVOLVER : RoomEnum.BILLIARD_ROOM, 
                                  WeaponEnum.WRENCH : RoomEnum.CONSERVATORY, 
                                  WeaponEnum.KNIFE : RoomEnum.KITCHEN}
        
        # Set turn order
        self._turn_order = [PlayerEnum.MISS_SCARLET, 
                            PlayerEnum.COLONEL_MUSTARD, 
                            PlayerEnum.MRS_WHITE, 
                            PlayerEnum.MR_GREEN, 
                            PlayerEnum.MRS_PEACOCK, 
                            PlayerEnum.PROFESSOR_PLUM]
        self._current_turn = 0
        
        self._suggest_player = PlayerEnum.MISS_SCARLET
        self._current_suggest = 0
        self._suggestion = []
        
        # Create gameboard
        self._gameboard = Gameboard()
        self._gameboard.setup_rooms()
        
        # Fill envelope with suspect, weapon, and room
        suspect = randint(1, 6)
        weapon = randint(1, 6)
        room = randint(1, 9)
        
        self._envelope = [suspect, weapon, room]
        
        self._game_started = False
    
    # Get the player_enum of who initiated the suggestion
    def get_suggester(self):
        return self._suggest_character
    
    # Set the player_enum to who initiated the suggestion
    def set_suggester(self, character):
        self._suggest_character = character
        
        self._current_suggest = self._current_turn
    
    # Get the next player_enum in the turn list
    def get_next_suggest_character(self):
        self._current_suggest += 1
        self._current_suggest = self._current_suggest % 6
        
        return self._turn_order[self._current_suggest]
    
    def get_suggestion(self):
        return self._suggestion
    
    def set_suggestion(self, suggestion):
        self._suggestion = suggestion
    
    # returns the player whose turn it is
    def get_turn_character(self):
        return self._turn_order[self._current_turn]
    
    # increases the turn pointer
    def change_turn_character(self):
        self._current_turn += 1
        self._current_turn = self._current_turn % 6
    
    # Add a player to the player list using the given address
    def add_player(self, address):
        # Assign an available player_enum from the character list to the new player
        for character in self._character_list:
            if self._character_list[character] == False:
                self._character_list[character] = True
                
                break
        
        # Find an available weapon_enum
        while 1:
            player_enum = randint(1, 6)
            
            if self._player_enum_list[player_enum] == False:
                self._player_enum_list[player_enum] = True
                break
        
        # Find an available weapon_enum
        while 1:
            weapon_enum = randint(1, 6)
            
            if self._weapon_enum_list[weapon_enum] == False:
                self._weapon_enum_list[weapon_enum] = True
                break
        
        # Find an available room
        while 1:
            room_enum = randint(1, 9)
            
            if self._room_enum_list[room_enum] == False:
                self._room_enum_list[room_enum] = True
                break
        
        new_player = Player(address, character, player_enum, weapon_enum, room_enum)
        
        # Add the new player to the player list
        character_str = PlayerEnum.to_string(character)
        player_enum_str = PlayerEnum.to_string(player_enum)
        weapon_enum_str = WeaponEnum.to_string(weapon_enum)
        room_enum_str = RoomEnum.to_string(room_enum)
        
        self._logger.debug('Adding (%s, %s) to player list as %s with cards (%s, %s, %s).', address[0], address[1], character_str, player_enum_str, weapon_enum_str, room_enum_str)
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
                # Make the character, player, weapon, and room available to be used by someone else
                character = player.get_character()
                self._character_list[character] = False
                
                player_enum = player.get_player_enum()
                self._player_enum_list[player_enum] = False
                
                weapon_enum = player.get_weapon_enum()
                self._weapon_enum_list[weapon_enum] = False
                
                room_enum = player.get_room_enum()
                self._room_enum_list[room_enum] = False
                
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
    def perform_move(self, character, destination_room):
        current_room = self._character_positions[character]
        
        character_str = PlayerEnum.to_string(character)
        current_room_str = RoomEnum.to_string(current_room)
        destination_room_str = RoomEnum.to_string(destination_room)
        self._logger.debug('Attempting to move %s from "%s" to "%s".', character_str, current_room_str, destination_room_str)
        
        # Check to see if the move is valid on the gameboard
        valid_move = self._gameboard.is_valid_move(current_room, destination_room)
        
        # Check to see if the destination is an occupied hallway
        if self._gameboard.is_hallway(destination_room) == True:
            for temp, character_location in self._character_positions.items():
                if destination_room == character_location:
                    valid_move = False
                    
                    break
        
        # Update the player position if the move is valid
        if valid_move == True:
            self._character_positions[character] = destination_room
        
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
    def get_character_position(self, character):
        current_room = self._character_positions[character]
        
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
            