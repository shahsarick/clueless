#!/usr/bin/env python

class RoomEnum(object):
    STUDY = 1
    HALL = 2
    LOUNGE = 3
    DINING_ROOM = 4
    KITCHEN = 5
    BALLROOM = 6
    CONSERVATORY = 7
    LIBRARY = 8
    BILLIARD_ROOM = 9
    HALLWAY_STUDY_HALL = 10
    HALLWAY_HALL_LOUNGE = 11
    HALLWAY_LOUNGE_DINING_ROOM = 12
    HALLWAY_DINING_ROOM_KITCHEN = 13
    HALLWAY_KITCHEN_BALLROOM = 14
    HALLWAY_BALLROOM_CONSERVATORY = 15
    HALLWAY_CONSERVATORY_LIBRARY = 16
    HALLWAY_LIBRARY_STUDY = 17
    HALLWAY_BILLIARD_ROOM_HALL = 18
    HALLWAY_BILLIARD_ROOM_DINING_ROOM = 19
    HALLWAY_BILLIARD_ROOM_BALLROOM = 20
    HALLWAY_BILLIARD_ROOM_LIBRARY = 21
    
    @staticmethod
    def to_string(room_enum):
        if room_enum == RoomEnum.STUDY:
            return 'Study'
        elif room_enum == RoomEnum.HALL:
            return 'Hall'
        elif room_enum == RoomEnum.LOUNGE:
            return 'Lounge'
        elif room_enum == RoomEnum.DINING_ROOM:
            return 'Dining room'
        elif room_enum == RoomEnum.KITCHEN:
            return 'Kitchen'
        elif room_enum == RoomEnum.BALLROOM:
            return 'Ballroom'
        elif room_enum == RoomEnum.CONSERVATORY:
            return 'Conservatory'
        elif room_enum == RoomEnum.LIBRARY:
            return 'Library'
        elif room_enum == RoomEnum.BILLIARD_ROOM:
            return 'Billiard room'
        elif room_enum == RoomEnum.HALLWAY_STUDY_HALL:
            return 'Study-Hall hallway'
        elif room_enum == RoomEnum.HALLWAY_HALL_LOUNGE:
            return 'Hall-Lounge hallway'
        elif room_enum == RoomEnum.HALLWAY_LOUNGE_DINING_ROOM:
            return 'Lounge-Dining room hallway'
        elif room_enum == RoomEnum.HALLWAY_DINING_ROOM_KITCHEN:
            return 'Dining room-Kitchen hallway'
        elif room_enum == RoomEnum.HALLWAY_KITCHEN_BALLROOM:
            return 'Kitchen-Ballroom hallway'
        elif room_enum == RoomEnum.HALLWAY_BALLROOM_CONSERVATORY:
            return 'Ballroom-Conservatory hallway'
        elif room_enum == RoomEnum.HALLWAY_CONSERVATORY_LIBRARY:
            return 'Conservatory-Library hallway'
        elif room_enum == RoomEnum.HALLWAY_LIBRARY_STUDY:
            return 'Library-Study hallway'
        elif room_enum == RoomEnum.HALLWAY_BILLIARD_ROOM_HALL:
            return 'Billiard room-Hall hallway'
        elif room_enum == RoomEnum.HALLWAY_BILLIARD_ROOM_DINING_ROOM:
            return 'Billiard room-Dining room hallway'
        elif room_enum == RoomEnum.HALLWAY_BILLIARD_ROOM_BALLROOM:
            return 'Billiard room-Ballroom hallway'
        elif room_enum == RoomEnum.HALLWAY_BILLIARD_ROOM_LIBRARY:
            return 'Billiard room-Library hallway'
        else:
            return ''