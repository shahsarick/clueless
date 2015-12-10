#!/usr/bin/env python

import cPickle as pickle
import logging
import select
import socket
import threading

from common.Message import Message
from common.MessageEnum import MessageEnum

from server.ServerMessage import ServerMessage

class CluelessServer:
    __connection_backlog = 10
    __select_timeout = 0.5
    __read_size = 4096

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._socket_list = []
        
        self._logger = logging.getLogger('CluelessServer')
        
        self._server_message = ServerMessage()
    
    def start_server(self):
        # Create the server socket
        self._logger.debug('Creating server socket.')
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Listen for connections
        self._logger.debug('Listening for connections.')
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen(self.__connection_backlog)
        
        self._socket_list.append(self._server_socket)
        
        server_thread = threading.Thread(target=self.run)
        server_thread.start()
    
    def run(self):
        while True:
            ready_to_read, ready_to_write, input_error = select.select(self._socket_list, [], [], self.__select_timeout)
            
            # Loop through list of sockets that have data
            for sock in ready_to_read:
                # Received new connection request
                if sock == self._server_socket:
                    # Accept the connection and append it to the socket list
                    self._logger.debug('Received connection request. Establishing connection with client.')
                    sock_fd, address = self._server_socket.accept()
                    
                    # Check the number of players currently connected to the server
                    if len(self._socket_list) < 7:
                        self._logger.debug('Client connected from %s on port %s' % address)
                        
                        # Add the socket to the socket list
                        self._socket_list.append(sock_fd)
                        
                        # Add a new player to the server model
                        self._server_message.add_player(address)
                    # Game is full
                    else:
                        self._logger.debug('Closed connection with %s on port %s' % address)
                        
                        sock_fd.close()
                # Received message from client
                else:
                    # Retrieve the player associated with this socket
                    player = self._server_message.get_player(sock._sock.getpeername()[0])
                    
                    # Read message
                    try:
                        #TODO: Loop to make sure we get all of the data from socket
                        data_string = sock.recv(self.__read_size)
                        
                        # Data available
                        if data_string:
                            self._logger.debug('Received message from %s.', player.get_ip())
                            
                            # Deserialize the message
                            message = pickle.loads(data_string)
                            
                            # Handle the request
                            broadcast, response = self._server_message.handle_message(message, player)
                            
                            # Send a response to the client(s)
                            self._logger.debug('Sending message to client(s).')
                            
                            self.send_message(broadcast, sock, response)
                        # Client disconnected
                        else:
                            self._logger.error('Client disconnected.')
                            self.remove_client(sock)
                    except:
                        self._logger.error('Exception occurred while reading data from %s.', player.get_ip())
                        self.remove_client(sock)
                        
                        continue
        
        self._server_socket.close()
    
    def send_message(self, broadcast, sock, response):
        data_string = pickle.dumps(response)
        
        if broadcast == True:
            for client_socket in self._socket_list:
                #TODO: Should broadcast skip sending a message to the player who initiated the action?
                if client_socket != self._server_socket:
                    client_socket.sendall(data_string)
        else:
            sock.sendall(data_string)
    
    def remove_client(self, sock):
        peername = sock._sock.getpeername()[0]
        self._logger.debug('Removing the connection to %s.', peername)
        
        self._socket_list.remove(sock)
        self._server_message.remove_player(peername)
        
        sock.close()