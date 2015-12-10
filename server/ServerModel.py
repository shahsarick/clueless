#!/usr/bin/env python

import logging

from common.Player import Player

class ServerModel:
    
    def __init__(self):
        self._logger = logging.getLogger('ServerModel')
        
        self._player_list = []
    
    def add_player(self, address):
        self._logger.debug('Adding (%s, %s) to player list.' % address)
        
        new_player = Player(address)
        self._player_list.append(new_player)
    
    def get_player(self, ip):
        self._logger.debug('Retrieving player mapped to %s.', ip)
        
        for player in self._player_list:
            if ip == player.get_ip():
                return player
    
    def remove_player(self, ip):
        self._logger.debug('Removing %s from player list.', ip)
        
        for player in self._player_list:
            if ip == player.get_ip():
                self._player_list.remove(player)
    
    def get_lobby_list(self):
        self._logger.debug('Retrieving lobby list:')
        
        lobby_list = []
        
        for player in self._player_list:
            player_name = player.get_name()
            ready_state = player.get_ready_status()
            self._logger.debug('\t(%s, %s)', player_name, ready_state)
            
            lobby_entry = [player_name, ready_state]
            lobby_list.append(lobby_entry)
        
        return lobby_list
            