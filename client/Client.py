#!/usr/bin/env python

import logging
import select
import socket
import sys
import time
from observer.observer import observerObject

# reference the subject
obsObj = observerObject()

class Client:
    __socket_timeout = 2
    __select_timeout = 0.5
    __read_size = 4096
    
    def __init__(self, input_queue, send_queue):
        self._logger = logging.getLogger('Client')
        
        self._input_queue = input_queue
        self._output_queue = send_queue
    
    # Connect to the server
    def connect_to_server(self, host, port):
        # Create the client socket
        self._logger.debug('Creating client socket.')
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.settimeout(self.__socket_timeout)
        
        # Attempt to connect to the server
        self._logger.debug('Attempting to connect to server.')
        
        try:
            self._client_socket.connect((host, port))
        except:
            self._logger.error('Unable to connect to the server.')
            
            return False
        
        self._logger.debug('Connected to %s on port %s', host, port)
        
        return True
    
    def run(self):
        while True:
            fd_list = [self._client_socket]
            
            # Get the list of sockets that are readable
            ready_to_read, ready_to_write, input_error = select.select(fd_list, [], [], self.__select_timeout)
            
            for fd in ready_to_read:
                # Received message from server
                if fd == self._client_socket:

                    # This should ensure all the data from the socket is received
                    total_data = []
                    begin = time.time()
                    # same as while True but faster
                    while 1:
                        # you have data and timeout has occured since getting data
                        if total_data and time.time()-begin > self.__select_timeout:
                            break
                        # wait longer if no data received
                        elif time.time()-begin > self.__select_timeout * 2:
                            break

                        try:
                            data_string = self._client_socket.recv(self.__read_size)
                            if data_string:
                                total_data.append(data_string)
                                begin = time.time()
                            else:
                                time.sleep(0.1)
                        except:
                            pass
                    data_string = ''.join(total_data)

                    # Data available
                    if data_string:
                        # Place the server message into the output queue and notify the client that data has been received
                        self._output_queue.put(data_string)
                        self.notify_client_message()
                    # Disconnected from server
                    else:
                        self._logger.error('Disconnected from the server.')
                        sys.exit()
            
            # Check to see if data is available on the input queue
            # Note: Normally the queue would be in the select call, but I don't think 
            #       Queue is implemented as a file descriptor in Python (or Windows sucks)
            if self._input_queue.qsize() > 0:
                self._logger.debug('Retrieving message from input queue.')
                
                try:
                    data_string = self._input_queue.get_nowait()
                except:
                    break
                
                # Send message to the server
                self._logger.debug('Sending message to server.')
                self._client_socket.sendall(data_string)

    # only called if there is a message in the queue
    def notify_client_message(self):
        obsObj.subject.notify_observers()