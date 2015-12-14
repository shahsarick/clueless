#!/usr/bin/env python

class Player:

    def __init__(self, character):
        self._character = character
        
        self._player_enum_list = []
        self._weapon_enum_list = []
        self._room_enum_list = []
        
        self.reset_player()
    
    def get_address(self):
        return self._address
    
    def set_address(self, address):
        self._address = address
    
    def get_character(self):
        return self._character
    
    def set_character(self, character):
        self._character = character
    
    def get_player_enum_list(self):
        return self._player_enum_list
    
    def add_player_enum(self, player_enum):
        self._player_enum_list.append(player_enum)
    
    def get_weapon_enum_list(self):
        return self._weapon_enum_list
    
    def add_weapon_enum(self, weapon_enum):
        self._weapon_enum_list.append(weapon_enum)
    
    def get_room_enum_list(self):
        return self._room_enum_list
    
    def add_room_enum(self, room_enum):
        self._room_enum_list.append(room_enum)
    
    def get_name(self):
        return self._player_name
    
    def set_name(self, player_name):
        self._player_name = player_name
    
    def get_ready_status(self):
        return self._ready_state
    
    def set_ready_status(self, ready_state):
        self._ready_state = ready_state
    
    def is_connected(self):
        return self._is_connected
    
    def set_connected(self):
        self._is_connected = True
    
    def reset_player(self):
        self._player_name = ''
        self._ready_state = True
        self._is_connected = False