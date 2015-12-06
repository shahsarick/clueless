#!/usr/bin/env python

class Message:
    
    def __init__(self, message_enum, num_args, packet_string):
        self._message_enum = message_enum
        self._num_args = num_args
        self._packet_string = packet_string
    
    def get_message_contents(self):
        return (self._message_enum, self._num_args, self._packet_string)
    
    def get_message_enum(self):
        return self._message_enum