#!/usr/bin/env python

import logging

from common.Room import Room
from common.RoomEnum import RoomEnum

class Gameboard:
    
    def __init__(self):
        self._logger = logging.getLogger('Gameboard')
    
    # Setup the rooms
    def setup_rooms(self):
        self._logger.debug('Setting up gameboard.')
        
        # Create Study
        study = Room([RoomEnum.HALLWAY_STUDY_HALL, \
                      RoomEnum.HALLWAY_LIBRARY_STUDY, \
                      RoomEnum.KITCHEN])
        
        # Create Hall
        hall = Room([RoomEnum.HALLWAY_HALL_LOUNGE, \
                     RoomEnum.HALLWAY_BILLIARD_ROOM_HALL, \
                     RoomEnum.HALLWAY_STUDY_HALL])
        
        # Create Lounge
        lounge = Room([RoomEnum.HALLWAY_LOUNGE_DINING_ROOM, \
                       RoomEnum.HALLWAY_HALL_LOUNGE, \
                       RoomEnum.CONSERVATORY])
        
        # Create Dining room
        dining_room = Room([RoomEnum.HALLWAY_LOUNGE_DINING_ROOM, \
                            RoomEnum.HALLWAY_DINING_ROOM_KITCHEN, \
                            RoomEnum.HALLWAY_BILLIARD_ROOM_DINING_ROOM])
        
        # Create Kitchen
        kitchen = Room([RoomEnum.HALLWAY_DINING_ROOM_KITCHEN, \
                        RoomEnum.HALLWAY_KITCHEN_BALLROOM, \
                        RoomEnum.STUDY])
        
        # Create Ballroom
        ballroom = Room([RoomEnum.HALLWAY_BILLIARD_ROOM_BALLROOM, \
                         RoomEnum.HALLWAY_KITCHEN_BALLROOM, \
                         RoomEnum.HALLWAY_BALLROOM_CONSERVATORY])
        
        # Create Conservatory
        conservatory = Room([RoomEnum.HALLWAY_CONSERVATORY_LIBRARY, \
                             RoomEnum.HALLWAY_BALLROOM_CONSERVATORY, \
                             RoomEnum.LOUNGE])
        
        # Create Library
        library = Room([RoomEnum.HALLWAY_LIBRARY_STUDY, \
                        RoomEnum.HALLWAY_BILLIARD_ROOM_LIBRARY, \
                        RoomEnum.HALLWAY_CONSERVATORY_LIBRARY])
        
        # Create Billiard room
        billiard_room = Room([RoomEnum.HALLWAY_BILLIARD_ROOM_HALL, \
                              RoomEnum.HALLWAY_BILLIARD_ROOM_DINING_ROOM, \
                              RoomEnum.HALLWAY_BILLIARD_ROOM_BALLROOM, \
                              RoomEnum.HALLWAY_BILLIARD_ROOM_LIBRARY])
        
        # Create hallways
        hallway_study_hall = Room([RoomEnum.STUDY, RoomEnum.HALL])
        hallway_hall_lounge = Room([RoomEnum.HALL, RoomEnum.LOUNGE])
        hallway_lounge_dining_room = Room([RoomEnum.LOUNGE, RoomEnum.DINING_ROOM])
        hallway_dining_room_kitchen = Room([RoomEnum.DINING_ROOM, RoomEnum.KITCHEN])
        hallway_kitchen_ballroom = Room([RoomEnum.KITCHEN, RoomEnum.BALLROOM])
        hallway_ballroom_conservatory = Room([RoomEnum.BALLROOM, RoomEnum.CONSERVATORY])
        hallway_conservatory_library = Room([RoomEnum.CONSERVATORY, RoomEnum.LIBRARY])
        hallway_library_study = Room([RoomEnum.LIBRARY, RoomEnum.STUDY])
        hallway_billiard_room_hall = Room([RoomEnum.BILLIARD_ROOM, RoomEnum.HALL])
        hallway_billiard_room_dining_room = Room([RoomEnum.BILLIARD_ROOM, RoomEnum.DINING_ROOM])
        hallway_billiard_room_ballroom = Room([RoomEnum.BILLIARD_ROOM, RoomEnum.BALLROOM])
        hallway_billiard_room_library = Room([RoomEnum.BILLIARD_ROOM, RoomEnum.LIBRARY])
        
        # Create room dictionary
        self._rooms = {RoomEnum.STUDY : study, \
                       RoomEnum.HALL : hall, \
                       RoomEnum.LOUNGE : lounge, \
                       RoomEnum.DINING_ROOM : dining_room, \
                       RoomEnum.KITCHEN : kitchen, \
                       RoomEnum.BALLROOM : ballroom, \
                       RoomEnum.CONSERVATORY : conservatory, \
                       RoomEnum.LIBRARY : library, \
                       RoomEnum.BILLIARD_ROOM : billiard_room, \
                       RoomEnum.HALLWAY_STUDY_HALL : hallway_study_hall, \
                       RoomEnum.HALLWAY_HALL_LOUNGE : hallway_hall_lounge, \
                       RoomEnum.HALLWAY_LOUNGE_DINING_ROOM : hallway_lounge_dining_room, \
                       RoomEnum.HALLWAY_DINING_ROOM_KITCHEN : hallway_dining_room_kitchen, \
                       RoomEnum.HALLWAY_KITCHEN_BALLROOM : hallway_kitchen_ballroom, \
                       RoomEnum.HALLWAY_BALLROOM_CONSERVATORY : hallway_ballroom_conservatory, \
                       RoomEnum.HALLWAY_CONSERVATORY_LIBRARY : hallway_conservatory_library, \
                       RoomEnum.HALLWAY_LIBRARY_STUDY : hallway_library_study, \
                       RoomEnum.HALLWAY_BILLIARD_ROOM_HALL : hallway_billiard_room_hall, \
                       RoomEnum.HALLWAY_BILLIARD_ROOM_DINING_ROOM : hallway_billiard_room_dining_room, \
                       RoomEnum.HALLWAY_BILLIARD_ROOM_BALLROOM : hallway_billiard_room_ballroom, \
                       RoomEnum.HALLWAY_BILLIARD_ROOM_LIBRARY : hallway_billiard_room_library}
    
    # Check to see if a move from the current room to the destination room is valid
    def is_valid_move(self, current_room, destination_room):
        room = self._rooms[current_room]
        
        current_room_str = RoomEnum.to_string(current_room)
        destination_room_str = RoomEnum.to_string(destination_room)
        self._logger.debug('Determining if move from "%s" to "%s" is valid.', current_room_str, destination_room_str)
        
        valid_move = room.is_valid_move(destination_room)
        
        return valid_move
    
    # Retrieve the list of rooms connected to the current room
    def get_valid_moves(self, current_room):
        room = self._rooms[current_room]
        
        valid_room_list = room.get_valid_moves()
        
        return valid_room_list