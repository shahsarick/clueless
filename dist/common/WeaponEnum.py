#!/usr/bin/env python

class WeaponEnum(object):
    CANDLESTICK = 1
    ROPE = 2
    LEAD_PIPE = 3
    REVOLVER = 4
    WRENCH = 5
    KNIFE = 6
    
    @staticmethod
    def to_string(weapon_enum):
        if weapon_enum == WeaponEnum.CANDLESTICK:
            return 'Candlestick'
        elif weapon_enum == WeaponEnum.ROPE:
            return 'Rope'
        elif weapon_enum == WeaponEnum.LEAD_PIPE:
            return 'Lead pipe'
        elif weapon_enum == WeaponEnum.REVOLVER:
            return 'Revolver'
        elif weapon_enum == WeaponEnum.WRENCH:
            return 'Wrench'
        elif weapon_enum == WeaponEnum.KNIFE:
            return 'Knife'
        else:
            return ''