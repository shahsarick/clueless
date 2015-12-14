#!/usr/bin/env python

class MessageEnum(object):
    MOVE = 1
    SUGGEST = 2
    SUGGESTION_BEGIN = 3
    SUGGESTION_END = 4
    ACCUSE = 5
    LOBBY_ADD = 6
    LOBBY_READY = 7
    LOBBY_UNREADY = 8
    LOBBY_CHANGE_PLAYER = 9
    GAME_STATE_CHANGE = 10
    TURN_OVER = 11
    TURN_BEGIN = 12
    ERROR = 13