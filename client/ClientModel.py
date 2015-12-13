#!/usr/bin/env python
class ClientModel:
    
    def __init__(self):
        self.moved_to_room = False
        self.has_moved = False
        self.has_suggested = False
        self.has_accused = False
        self.must_suggest = False
    
    # Gets the player_enum
    def get_player_enum(self):
        return self._player_enum
    
    # Sets the player_enum
    def set_player_enum(self, player_enum):
        self._player_enum = player_enum

    def moved_to_room(self, bool):
        if bool == True:
            self.moved_to_room = True
        else:
            self.moved_to_room = False
    def set_has_moved(self, bool):
        if bool == True:
            self.has_moved = True
        else:
            self.has_moved = False
    def reset_all(self):
        self.has_moved = False
        self.has_suggested = False
        self.has_accused = False