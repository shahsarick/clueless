#!/usr/bin/env python

class Player:

    def __init__(self, address, player_enum, weapon_enum, room_enum):
        self._address = address
        self._player_enum = player_enum
        self._weapon_enum = weapon_enum
        self._room_enum = room_enum
        
        self._player_name = ''
        self._ready_state = False
    
    def get_address(self):
        return self._address
    
    def get_player_enum(self):
        return self._player_enum
    
    def set_player_enum(self, player_enum):
        self._player_enum = player_enum
    
    def get_weapon_enum(self):
        return self._weapon_enum
    
    def set_weapon_enum(self, weapon_enum):
        self._weapon_enum = weapon_enum
    
    def get_room_enum(self):
        return self._room_enum
    
    def set_room_enum(self, room_enum):
        self._room_enum = room_enum
    
    def get_name(self):
        return self._player_name
    
    def set_name(self, player_name):
        self._player_name = player_name
    
    def get_ready_status(self):
        return self._ready_state
    
    def set_ready_status(self, ready_state):
        self._ready_state = ready_state