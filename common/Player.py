#!/usr/bin/env python

from common.PlayerEnum import PlayerEnum

class Player:

    def __init__(self, character):
        self._character = character
        
        self._player_enum_list = []
        self._weapon_enum_list = []
        self._room_enum_list = []
        
        self.reset_player()
    
    # Gets the IP and port for the player associated with this player entry
    def get_address(self):
        return self._address
    
    # Sets the IP and port for the player being associated with this player entry
    def set_address(self, address):
        self._address = address
    
    # Gets the character token for this player
    def get_character(self):
        return self._character
    
    # Sets the character token for this player
    def set_character(self, character):
        self._character = character
    
    # Gets the list of player_enum cards held by this player
    def get_player_enum_list(self):
        return self._player_enum_list
    
    # Sets the list of player_enum cards held by this player
    def add_player_enum(self, player_enum):
        self._player_enum_list.append(player_enum)
    
    # Gets the list of weapon cards held by this player
    def get_weapon_enum_list(self):
        return self._weapon_enum_list
    
    # Sets the list of weapon cards held by this player
    def add_weapon_enum(self, weapon_enum):
        self._weapon_enum_list.append(weapon_enum)
    
    # Gets the list of room cards held by this player
    def get_room_enum_list(self):
        return self._room_enum_list
    
    # Sets the list of room cards held by this player
    def add_room_enum(self, room_enum):
        self._room_enum_list.append(room_enum)
    
    # Retrieves a list of the cards this player has
    def get_cards(self):
        return (self._player_enum_list, self._weapon_enum_list, self._room_enum_list)
    
    # Gets the name
    def get_name(self):
        return self._player_name
    
    # Sets the name
    def set_name(self, player_name):
        self._player_name = player_name
    
    # Gets the ready status
    def get_ready_status(self):
        return self._ready_state
    
    # Sets the ready status
    def set_ready_status(self, ready_state):
        self._ready_state = ready_state
    
    # Checks to see if a player is connected to this player entry
    def is_connected(self):
        return self._is_connected
    
    # Sets the connected state
    def set_connected(self, connected):
        self._is_connected = connected
    
    # Reset the player entry attributes associated with a connected player 
    def reset_player(self):
        self._player_name = PlayerEnum.to_string(self._character)
        self._ready_state = True
        self._is_connected = False