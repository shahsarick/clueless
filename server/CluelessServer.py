#!/usr/bin/env python

import cPickle as pickle
import logging
import select
import socket
import threading

from common.Message import Message
from common.MessageEnum import MessageEnum

from server.ServerMessage import ServerMessage
from server.ServerModel import ServerModel

class CluelessServer:
    __connection_backlog = 10
    __select_timeout = 0.5
    __read_size = 4096

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._socket_list = []
        
        self._logger = logging.getLogger('CluelessServer')
        
        #TODO: Move server model into servermessage (message will perform the processing and update the model)
        self._server_model = ServerModel()
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
                    self._logger.debug('Client connected from %s on port %s' % address)
                    
                    # Add the socket to the socket list
                    self._socket_list.append(sock_fd)
                    
                    # Add a new player to the server model
                    self._server_model.add_player(address)
                # Received message from client
                else:
                    # Retrieve the player associated with this socket
                    #TODO: Remove this step if we do not need any player information at this level
                    player = self._server_model.get_player(sock._sock.getpeername()[0])
                    
                    # Read message
                    try:
                        #TODO: Loop to make sure we get all of the data from socket
                        data_string = sock.recv(self.__read_size)
                        
                        # Data available
                        if data_string:
                            # Deserialize the message
                            self._logger.debug('Reading data from socket.')
                            message = pickle.loads(data_string)
                            message_enum, num_args, packet_string = message.get_message_contents()
                            self._logger.debug('Request from %s: "%s, %s, %s"', player.get_ip(), message_enum, num_args, packet_string)
                            
                            # Handle the request
                            self._server_message.handle_message(message)
                            
                            # Respond to client
                            message = Message(MessageEnum.TURN_OVER, 1, 'Your turn is over!')
                            data_string = pickle.dumps(message)
                            sock.sendall(data_string)
                        # Client disconnected
                        else:
                            self._logger.error('Client disconnected.')
                            self.remove_client(sock)
                    except:
                        self._logger.error('Exception occurred while reading data from %s.', player.get_ip())
                        self.remove_client(sock)
                        
                        continue
        
        self._server_socket.close()
    
    def remove_client(self, sock):
        peername = sock._sock.getpeername()[0]
        self._logger.debug('Removing the connection to %s.', peername)
        
        self._socket_list.remove(sock)
        self._server_model.remove_player(peername)
        
        sock.close()