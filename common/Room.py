#!/usr/bin/env python

class Room:
    
    def __init__(self, room_list):
        self._connected_rooms = room_list
    
    # Check to see if a move to the destination room is valid
    def is_valid_move(self, destination_room):
        # Check to see if the destination room matches any of the rooms connected to this one
        for room in self._connected_rooms:
            if room == destination_room:
                return True
        
        return False
    
    # Retrieve the list of rooms connected to this one
    def get_valid_moves(self):
        return self._connected_rooms