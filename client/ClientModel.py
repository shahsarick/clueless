#!/usr/bin/env python

from common.Gameboard import Gameboard
from common.PlayerEnum import PlayerEnum
from common.RoomEnum import RoomEnum
from common.WeaponEnum import WeaponEnum

class ClientModel:
    
    def __init__(self):
        self._moved_to_room = False
        self._has_moved = False
        self._has_suggested = False
        self._has_accused = False
        self._must_suggest = False
        
        self._suggestion = []
        
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
        
        self._gameboard = Gameboard()
        self._gameboard.setup_rooms()
    
    # Gets the player_enum
    def get_player_enum(self):
        return self._player_enum
    
    # Sets the player_enum
    def set_player_enum(self, player_enum):
        self._player_enum = player_enum
    
    # Gets the weapon enum
    def get_weapon_enum(self):
        return self._weapon_enum
    
    # Sets the weapon enum
    def set_weapon_enum(self, weapon_enum):
        self._weapon_enum = weapon_enum
    
    # Gets the room enum
    def get_room_enum(self):
        return self._room_enum
    
    # Sets the room enum
    def set_room_enum(self, room_enum):
        self._room_enum = room_enum
    
    # Move the specified player to the specified room
    def move_player(self, player_enum, room):
        # Update player position
        self._player_positions[player_enum] = room
        
        # Check to see if the player that moved is this player
        if self._player_enum == player_enum:
            self._has_moved = True
            
            # update the in-room status of the client
            if self._gameboard.is_hallway(room) == True:
                self._moved_to_room = False;
            else:
                self._moved_to_room = True
                self._must_suggest = True
    
    # Retrieves the player position
    def get_player_position(self):
        player_enum = self._player_enum
        current_room = self._player_positions[player_enum]
        
        return current_room
    
    # Retrieve the move status for the player
    def get_suggest_status(self):
        return self._must_suggest
    
    def make_suggestion(self):
        self._has_suggested = False
        self._must_suggest = False
    
    def set_suggestion(self, suggestion):
        self._suggestion = suggestion
    
    def reset_all(self):
        self._has_moved = False
        self._has_suggested = False
        self._has_accused = False

    def set_accuse_status(self, bool):
        if bool == True:
            self._has_accused = True
        else:
            self._has_accused = False
