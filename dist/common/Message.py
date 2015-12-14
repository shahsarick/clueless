#!/usr/bin/env python

class Message:
    
    def __init__(self, message_enum, num_args, arg_list):
        self._message_enum = message_enum
        self._num_args = num_args
        self._arg_list = arg_list
    
    def get_message_contents(self):
        return (self._message_enum, self._num_args, self._arg_list)
    
    def get_message_enum(self):
        return self._message_enum
    
    def get_num_args(self):
        return self._num_args
    
    def get_args(self):
        return self._arg_list