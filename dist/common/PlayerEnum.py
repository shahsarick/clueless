#!/usr/bin/env python

class PlayerEnum(object):
    MISS_SCARLET = 1
    COLONEL_MUSTARD = 2
    PROFESSOR_PLUM = 3
    MR_GREEN = 4
    MRS_WHITE = 5
    MRS_PEACOCK = 6
    ENVELOPE = 7
    
    @staticmethod
    def to_string(player_enum):
        if player_enum == PlayerEnum.MISS_SCARLET:
            return 'Miss Scarlet'
        elif player_enum == PlayerEnum.COLONEL_MUSTARD:
            return 'Colonel Mustard'
        elif player_enum == PlayerEnum.PROFESSOR_PLUM:
            return 'Professor Plum'
        elif player_enum == PlayerEnum.MR_GREEN:
            return 'Mr. Green'
        elif player_enum == PlayerEnum.MRS_WHITE:
            return 'Mrs. White'
        elif player_enum == PlayerEnum.MRS_PEACOCK:
            return 'Mrs. Peacock'
        else:
            return ''