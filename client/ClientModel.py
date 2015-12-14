#!/usr/bin/env python

import logging

from common.Gameboard import Gameboard
from common.PlayerEnum import PlayerEnum
from common.RoomEnum import RoomEnum
from common.WeaponEnum import WeaponEnum

class ClientModel:
    
    def __init__(self):
        self._logger = logging.getLogger('ClientModel')
        
        self._won = None
        
        self._moved_to_room = False
        self._has_moved = False
        self._has_suggested = False
        self._has_accused = False
        self._must_suggest = False
        
        self._suggestion = []
        
        self._player_enum_list = []
        self._weapon_enum_list = []
        self._room_enum_list = []
        
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
        
        self._gameboard = Gameboard()
        self._gameboard.setup_rooms()
    
    # Get character token for this player
    def get_character(self):
        return self._character
    
    # Set character token for this player
    def set_character(self, character):
        self._character = character
    
    # Gets the player_enum
    def get_player_enum_list(self):
        return self._player_enum_list
    
    # Sets the player_enum
    def set_player_enum_list(self, player_enum_list):
        self._player_enum_list = player_enum_list
    
    # Gets the weapon enum
    def get_weapon_enum_list(self):
        return self._weapon_enum_list
    
    # Sets the weapon enum
    def set_weapon_enum_list(self, weapon_enum_list):
        self._weapon_enum_list = weapon_enum_list
    
    # Gets the room enum
    def get_room_enum_list(self):
        return self._room_enum_list
    
    # Sets the room enum
    def set_room_enum_list(self, room_enum_list):
        self._room_enum_list = room_enum_list
    
    # Move the specified character to the specified room
    def move_character(self, character, room):
        # Update player position
        self._character_positions[character] = room
        
        # Check to see if the player that moved is this player
        if self._character == character:
            self._has_moved = True
            
            # update the in-room status of the client
            if self._gameboard.is_hallway(room) == True:
                self._moved_to_room = False;
            else:
                self._moved_to_room = True
                self._must_suggest = True
    
    # Gets whether this player has moved, and if they were moved to a room
    def get_move_status(self):
        return (self._has_moved, self._moved_to_room)
    
    # Retrieves the player position
    def get_character_position(self):
        current_room = self._character_positions[self._character]
        
        return current_room
    
    # Retrieves a list of the cards this player has
    def get_cards(self):
        return (self._player_enum_list, self._weapon_enum_list, self._room_enum_list)
    
    # Retrieve the move status for the player
    def get_suggest_status(self):
        return self._must_suggest
    
    # Register that a suggestion is being made
    def make_suggestion(self):
        self._has_suggested = True
        self._must_suggest = False
    
    # Retrieves the current suggestion
    def get_suggestion(self):
        return self._suggestion
    
    # Sets the current suggestion
    def set_suggestion(self, suggestion):
        self._suggestion = suggestion
        
        character = suggestion[0]
        weapon = suggestion[1]
        room = suggestion[2]
        
        self._character_positions[character] = room
        self._weapon_locations[weapon] = room
        
        # Check to see if the character controlled by this player was moved by the suggestion
        if character == self._character:
            self._moved_to_room = True
    
    # Check to see if this player has made a suggestion
    def has_suggested(self):
        return self._has_suggested
    
    # Reset turn attributes
    def reset_all(self):
        self._has_moved = False
        self._has_suggested = False
        self._has_accused = False
        
    def set_accuse_status(self, accuse_status):
        self._has_accused = accuse_status
    
    # Returns whether the player has won or lost (None if neither)
    def has_won(self):
        return self._won
    
    # Sets whether the player has won or lost
    def set_won_game(self, win_status):
        self._won = win_status