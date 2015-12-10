#!/usr/bin/env python

class Player:

    def __init__(self, address):
        self._address = address
        
        self._ready_state = False
    
    def get_ip(self):
        return self._address[0]
    
    def get_player_enum(self):
        return self._player_enum
    
    def set_player_enum(self, player_enum):
        self._player_enum = player_enum
    
    def get_name(self):
        return self._player_name
    
    def set_name(self, player_name):
        self._player_name = player_name
    
    def get_ready_status(self):
        return self._ready_state
    
    def set_ready_status(self, ready_state):
        self._ready_state = ready_state