#!/usr/bin/env python

import cPickle as pickle
import logging
import Queue
import socket

from client.Client import Client

from common.Message import Message
from common.MessageEnum import MessageEnum

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

class ClientMessage:
    
    def __init__(self):
        host = socket.gethostbyname(socket.gethostname())
        port = 14415
        
        self._logger = logging.getLogger('ClientMessage')
        
        self._input_queue = Queue.Queue()
        self._output_queue = Queue.Queue()
        
        self._client = Client(host, port, self._input_queue, self._output_queue)
    
    def start_client(self):
        self._client.initialize()
    
    def send_message(self, user_input):
        message = Message(MessageEnum.TURN_BEGIN, 1, user_input)
        self._logger.debug('Sending data: "%s, %s, %s"' % message.get_message_contents())
        
        # Send message to server
        data_string = pickle.dumps(message)
        self._input_queue.put(data_string)
    
    def receive_message(self):
        data_string = self._output_queue.get()
        message = pickle.loads(data_string)
        self._logger.debug('Response from server: "%s, %s, %s"' % message.get_message_contents())