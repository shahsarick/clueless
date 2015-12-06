#!/usr/bin/env python

class MessageEnum(object):
    MOVE = 1
    SUGGEST = 2
    ACCUSE = 3
    LOBBY_ADD = 4
    LOBBY_READY = 5
    LOBBY_UNREADY = 6
    LOBBY_CHANGE_PLAYER = 7
    GAME_STATE_CHANGE = 8
    TURN_OVER = 9
    TURN_BEGIN = 10
    ERROR = 11