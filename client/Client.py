#!/usr/bin/env python

import logging
import select
import socket
import sys
import threading

from observer.observer import observerObject


# reference the subject
obsObj = observerObject()

class Client:
    __socket_timeout = 2
    __select_timeout = 0.5
    __read_size = 4096
    
    def __init__(self, host, port, input_queue, send_queue):
        self._host = host
        self._port = port
        
        self._logger = logging.getLogger('Client')
        
        self._input_queue = input_queue
        self._output_queue = send_queue
    
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
                    #TODO: Loop to make sure we get all of the data from socket
                    data_string = self._client_socket.recv(self.__read_size)
                    
                    # Data available
                    if data_string:
                        # Place the server message into the output queue and notify the client that data has been received
                        self._output_queue.put(data_string)
                        self.notify_client_message()
                    # Disconnected from server
                    else:
                        self._logger.error('Disconnected from the server.')
                        sys.exit()
            
            # Check to see if data needs to be sent to the server
            if self._input_queue.qsize() > 0:
                self._logger.debug('Retrieving message from input queue.')
                
                try:
                    data_string = self._input_queue.get_nowait()
                except:
                    break
                
                self._logger.debug('Sending message to server.')
                self._client_socket.sendall(data_string)

    # only called if there is a message in the queue
    def notify_client_message(self):
        obsObj.subject.notify_observers()