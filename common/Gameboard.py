#!/usr/bin/env python

from common.Room import Room
from common.RoomEnum import RoomEnum

class Gameboard:
    
    def __init__(self):
        pass
    
    # Setup the rooms
    def setup_rooms(self):
        # Create study
        study = Room([RoomEnum.HALLWAY_STUDY_HALL, \
                      RoomEnum.HALLWAY_LIBRARY_STUDY, \
                      RoomEnum.KITCHEN])
        
        # Create hall
        hall = Room([RoomEnum.HALLWAY_HALL_LOUNGE, \
                     RoomEnum.HALLWAY_BILLIARD_ROOM_HALL, \
                     RoomEnum.HALLWAY_STUDY_HALL])
        
        # Create lounge
        lounge = Room([RoomEnum.HALLWAY_LOUNGE_DINING_ROOM, \
                       RoomEnum.HALLWAY_HALL_LOUNGE, \
                       RoomEnum.CONSERVATORY])
        
        # Create dining room
        dining_room = Room([RoomEnum.HALLWAY_LOUNGE_DINING_ROOM, \
                            RoomEnum.HALLWAY_DINING_ROOM_KITCHEN, \
                            RoomEnum.HALLWAY_BILLIARD_ROOM_DINING_ROOM])
        
        # Create kitchen
        kitchen = Room([RoomEnum.HALLWAY_DINING_ROOM_KITCHEN, \
                        RoomEnum.HALLWAY_KITCHEN_BALLROOM, \
                        RoomEnum.STUDY])
        
        # Create ballroom
        ballroom = Room([RoomEnum.HALLWAY_BILLIARD_ROOM_BALLROOM, \
                         RoomEnum.HALLWAY_KITCHEN_BALLROOM, \
                         RoomEnum.HALLWAY_BALLROOM_CONSERVATORY])
        
        # Create conservatory
        conservatory = Room([RoomEnum.HALLWAY_CONSERVATORY_LIBRARY, \
                             RoomEnum.HALLWAY_BALLROOM_CONSERVATORY, \
                             RoomEnum.LOUNGE])
        
        # Create library
        library = Room([RoomEnum.HALLWAY_LIBRARY_STUDY, \
                        RoomEnum.HALLWAY_BILLIARD_ROOM_LIBRARY, \
                        RoomEnum.HALLWAY_CONSERVATORY_LIBRARY])
        
        # Create billiard room
        billiard_room = Room([RoomEnum.HALLWAY_BILLIARD_ROOM_HALL, \
                              RoomEnum.HALLWAY_BILLIARD_ROOM_DINING_ROOM, \
                              RoomEnum.HALLWAY_BILLIARD_ROOM_BALLROOM, \
                              RoomEnum.HALLWAY_BILLIARD_ROOM_LIBRARY])
        
        # Create room dictionary
        self._rooms = {RoomEnum.STUDY : study, \
                       RoomEnum.HALL : hall, \
                       RoomEnum.LOUNGE : lounge, \
                       RoomEnum.DINING_ROOM : dining_room, \
                       RoomEnum.KITCHEN : kitchen, \
                       RoomEnum.BALLROOM : ballroom, \
                       RoomEnum.CONSERVATORY : conservatory, \
                       RoomEnum.LIBRARY : library, \
                       RoomEnum.BILLIARD_ROOM : billiard_room}
    
    # Check to see if a move from the current room to the destination room is valid
    def is_valid_move(self, current_room, destination_room):
        room = self._rooms[current_room]
        
        valid_move = room.is_valid_move(destination_room)
        
        return valid_move
    
    # Retrieve the list of rooms connected to the current room
    def get_valid_moves(self, current_room):
        room = self._rooms[current_room]
        
        valid_room_list = room.get_valid_moves()
        
        return valid_room_list