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
        
        # Create the card dictionaries and player list
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
        
        self._player_list = [Player(PlayerEnum.MISS_SCARLET), 
                             Player(PlayerEnum.COLONEL_MUSTARD), 
                             Player(PlayerEnum.MRS_WHITE), 
                             Player(PlayerEnum.MR_GREEN), 
                             Player(PlayerEnum.MRS_PEACOCK), 
                             Player(PlayerEnum.PROFESSOR_PLUM)]
        
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
        
        self._game_started = False
        self._game_over = False
        
        # Create gameboard
        self._gameboard = Gameboard()
        self._gameboard.setup_rooms()
        
        # Handle cards
        self.fill_envelope()
        self.deal_cards()
    
    # Fills the envelope
    def fill_envelope(self):
        self._logger.debug('Filling envelope.')
        
        # Fill envelope with suspect, weapon, and room
        suspect = randint(1, 6)
        weapon = randint(1, 6)
        room = randint(1, 9)
        
        self._player_enum_list[suspect] = True
        self._weapon_enum_list[weapon] = True
        self._room_enum_list[room] = True
        
        self._envelope = [suspect, weapon, room]
    
    # Deals the cards to each player
    def deal_cards(self):
        self._logger.debug('Dealing cards to players.')
        
        player_index = 0
        
        while 1:
            # Get player to deal to
            player = self._player_list[player_index]
            
            # Get card type to deal
            card_added = False
            card_list = randint(1, 3)
            
            # Add a player card to the player
            if card_list == 1:
                # Check to see if this dictionary has cards available
                if self.dictionary_has_cards(self._player_enum_list) == True:
                    # Loop until we find a card available to deal
                    while 1:
                        player_enum = randint(1, 6)
                        
                        # Add card to player entry
                        if self._player_enum_list[player_enum] == False:
                            self._player_enum_list[player_enum] = True
                            player.add_player_enum(player_enum)
                            
                            card_added = True
                            break
            # Add a weapon card to the player 
            elif card_list == 2:
                # Check to see if this dictionary has cards available
                if self.dictionary_has_cards(self._weapon_enum_list) == True:
                    while 1:
                        weapon_enum = randint(1, 6)
                        
                        # Add card to player entry
                        if self._weapon_enum_list[weapon_enum] == False:
                            self._weapon_enum_list[weapon_enum] = True
                            player.add_weapon_enum(weapon_enum)
                            
                            card_added = True
                            break
            # Add a room to the player
            else:
                # Check to see if this dictionary has cards available
                if self.dictionary_has_cards(self._room_enum_list) == True:
                    while 1:
                        room_enum = randint(1, 9)
                        
                        # Add card to player entry
                        if self._room_enum_list[room_enum] == False:
                            self._room_enum_list[room_enum] = True
                            player.add_room_enum(room_enum)
                            
                            card_added = True
                            break
            
            # Increment player index
            if card_added == True:
                player_index += 1
                player_index = player_index % 6
            
            # Check to see if all cards have been dealt
            if self.dictionary_has_cards(self._player_enum_list) == False and \
               self.dictionary_has_cards(self._weapon_enum_list) == False and \
               self.dictionary_has_cards(self._room_enum_list) == False:
                break
    
    # Check to see if the dictionary has an available cards left to deal
    def dictionary_has_cards(self, dictionary):
        for entry in dictionary:
            if dictionary[entry] == False:
                return True
        
        return False
    
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
    
    # Retrieves the current suggestion
    def get_suggestion(self):
        return self._suggestion
    
    # Sets the current suggestion
    def set_suggestion(self, suggestion):
        self._suggestion = suggestion
        
        suspect = suggestion[0]
        weapon = suggestion[1]
        room = suggestion[2]
        
        self._character_positions[suspect] = room
        self._weapon_locations[weapon] = room
    
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
        for player in self._player_list:
            if player.is_connected() == False:
                player.set_connected(True)
                player.set_address(address)
                player.set_ready_status(False)
                
                break
        
        character = player.get_character()
        player_enum_list = player.get_player_enum_list()
        weapon_enum_list = player.get_weapon_enum_list()
        room_enum_list = player.get_room_enum_list()
        
        character_str = PlayerEnum.to_string(character)
        player_enum_list_str = ", ".join(PlayerEnum.to_string(pe) for pe in player_enum_list)
        weapon_enum_list_str = ", ".join(WeaponEnum.to_string(we) for we in weapon_enum_list)
        room_enum_list_str = ", ".join(RoomEnum.to_string(re) for re in room_enum_list)
        
        self._logger.debug('Adding (%s, %s) to player list as %s.', address[0], address[1], character_str)
        self._logger.debug('Player enum list: %s', player_enum_list_str)
        self._logger.debug('Weapon enum list: %s', weapon_enum_list_str)
        self._logger.debug('Room enum list: %s', room_enum_list_str)
    
    # Get the player with the associated address
    def get_player(self, address):
        for player in self._player_list:
            if player.is_connected() == True:
                player_address = player.get_address()
                
                if self.compare_addresses(address, player_address) == True:
                    return player
    
    # Retrieves the player from the player list using the specified character
    def get_player_from_character(self, character):
        for player in self._player_list:
            if player.get_character() == character:
                return player
    
    # Remove the player from the game
    def remove_player(self, address):
        self._logger.debug('Removing (%s, %s) from player list.' % address)
        
        for player in self._player_list:
            player_address = player.get_address()
            
            if self.compare_addresses(address, player_address) == True:
                # Reset the player information
                player.reset_player()
                
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
    
    # Perform a suggestion response for players that are not connected
    def perform_suggest(self, player):
        self._logger.debug('Attempting to disprove suggestion for %s.', PlayerEnum.to_string(player.get_character()))
        
        player_enum_list, weapon_list, room_list = player.get_cards()
        
        matched_args = [None, None, None]
        matched_player_enum = False
        matched_weapon = False
        matched_room = False
        disproven = False
        
        for player_enum in player_enum_list:
            if player_enum == self._suggestion[0]:
                matched_player_enum = True
                break
        
        for weapon in weapon_list:
            if weapon == self._suggestion[1]:
                matched_weapon = True
                break
        
        for room in room_list:
            if room == self._suggestion[2]:
                matched_room = True
                break
        
        if matched_player_enum == True or matched_weapon == True or matched_room == True:
            disproven = True
            matched = False
            
            while matched == False:
                choice = randint(1, 3)
                
                if choice == 1 and matched_player_enum == True:
                    matched = True
                    matched_args[0] = player_enum
                elif choice == 2 and matched_weapon == True:
                    matched = True
                    matched_args[1] = weapon
                elif choice == 3 and matched_room == True:
                    matched = True
                    matched_args[2] = room
        
        return (disproven, matched_args)
    
    # Get the list of players in the lobby and their associated ready status
    def get_lobby_list(self):
        self._logger.debug('Retrieving lobby list:')
        
        lobby_list = []
        
        for player in self._player_list:
            if player.is_connected() == True:
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
        connected_players = 0
        
        for player in self._player_list:
            if player.is_connected() == True:
                connected_players += 1
        
        if connected_players < 2:
            return False
        
        # Check to see if everyone in the game is ready
        for player in self._player_list:
            if player.is_connected() == True and player.get_ready_status() == False:
                return False
        
        self._game_started = True
        
        return True
    
    # Check to see if the game has started
    def is_game_started(self):
        return self._game_started
    
    # Check to see if the accusation is correct or not
    def check_accusation(self, suspect, weapon, room):
        if suspect == self._envelope[0] and weapon == self._envelope[1] and room == self._envelope[2]:
            self.set_game_over(self)
            
            return True
        else:
            return False
    
    # Sets the game over flag to true
    def set_game_over(self):
        self._game_over = True
        
        #TODO: Reset game to a new game?