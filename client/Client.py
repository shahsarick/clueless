#!/usr/bin/env python

import cPickle as pickle
import logging
import Queue
import select
import socket
import sys
import threading

from common.Message import Message
from common.MessageEnum import MessageEnum

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

class Client:
    __socket_timeout = 2
    __select_timeout = 0.5
    __read_size = 4096
    
    def __init__(self, host, port):
        self._host = host
        self._port = port
        
        self._logger = logging.getLogger('Client')
        
        self._output_queue = Queue.Queue()
    
    def initialize(self):
        # Create the client socket
        self._logger.debug('Creating client socket.')
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.settimeout(self.__socket_timeout)
        
        # Attempt to connect to the server
        self._logger.debug('Attempting to connect to server.')
        
        try:
            self._client_socket.connect((self._host, self._port))
        except:
            self._logger.error('Unable to connect to server.')
            sys.exit()
        
        self._logger.debug('Connected to %s on port %s', self._host, self._port)
        
        client_thread = threading.Thread(target=self.run)
        client_thread.start()
    
    def run(self):
        while True:
            fd_list = [self._client_socket]
            
            # Get the list of sockets that are readable
            ready_to_read, ready_to_write, input_error = select.select(fd_list, [], [], self.__select_timeout)
            
            for fd in ready_to_read:
                # Received message from server
                if fd == self._client_socket:
                    data_string = self._client_socket.recv(self.__read_size)
                    
                    # Data available
                    if data_string:
                        message = pickle.loads(data_string)
                        self._logger.debug('Response from server: "%s, %s, %s"' % message.get_message_contents())
                    # Disconnected from server
                    else:
                        self._logger.error('Disconnected from the server.')
                        sys.exit()
            
            # Check to see if data needs to be sent to the server
            if self._output_queue.qsize() > 0:
                self._logger.debug('Retrieving message from output queue.')
                
                try:
                    data_string = self._output_queue.get_nowait()
                except:
                    break
                
                self._logger.debug('Sending message to server.')
                self._client_socket.sendall(data_string)
    
    def send_message(self, data):
        message = Message(MessageEnum.TURN_BEGIN, 1, data)
        self._logger.debug('Sending data: "%s, %s, %s"' % message.get_message_contents())
        
        # Send message to server
        data_string = pickle.dumps(message)
        self._output_queue.put(data_string)