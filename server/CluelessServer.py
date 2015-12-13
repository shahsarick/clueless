#!/usr/bin/env python

import cPickle as pickle
import logging
import Queue
import select
import socket
import threading

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
        
        self._output_queue = Queue.Queue()
        
        self._server_message = ServerMessage(self._output_queue)
    
    # Starts the server
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
                    new_sock, address = self._server_socket.accept()
                    
                    # Check the number of players currently connected to the server
                    if len(self._socket_list) < 7:
                        self._logger.debug('Client connected from %s on port %s' % address)
                        
                        # Add the socket to the socket list
                        self._socket_list.append(new_sock)
                        
                        # Add a new player to the server model
                        self._server_message.add_player(address)
                        
                        # Send all messages in the output queue
                        self.send_all_messages(new_sock)
                    # Game is full
                    else:
                        self._logger.debug('Closed connection with %s on port %s' % address)
                        
                        new_sock.close()
                # Received message from client
                else:
                    # Retrieve the player associated with this socket
                    address = sock._sock.getpeername()
                    player = self._server_message.get_player(address)
                    
                    # Read message
                    try:
                        #TODO: Loop to make sure we get all of the data from socket
                        data_string = sock.recv(self.__read_size)
                        
                        # Data available
                        if data_string:
                            #TODO: Remove this debug statement?
                            self._logger.debug('Received message from (%s, %s).' % address)
                            
                            # Deserialize the message
                            message = pickle.loads(data_string)
                            
                            # Handle the request
                            self._server_message.handle_message(message, player)
                            
                            # Send response to the client(s)
                            self._logger.debug('Sending message(s) to client(s).')
                            
                            # Send all messages in the output queue
                            self.send_all_messages(sock)
                        # Client disconnected
                        else:
                            self._logger.error('Client disconnected.')
                            self.remove_client(sock)
                    except:
                        self._logger.error('Exception occurred while reading data from (%s, %s).' % address)
                        self.remove_client(sock)
                        
                        continue
        
        self._server_socket.close()
    
    # Send all of the messages in the output queue
    def send_all_messages(self, sock):
        while self._output_queue.qsize() > 0:
            broadcast, message = self._output_queue.get()
            self.send_message(broadcast, sock, message)
    
    # Sends a reply message or broadcasts the message to all clients
    def send_message(self, broadcast, sock, message):
        data_string = pickle.dumps(message)
        
        # Check to see if this is a broadcast message
        if broadcast == True:
            for client_socket in self._socket_list:
                #TODO: Should broadcast skip sending a message to the player who initiated the action?
                if client_socket != self._server_socket:
                    client_socket.sendall(data_string)
        # Send the message to the specified socket (sock)
        else:
            sock.sendall(data_string)
    
    # Remove the specified client from the server
    def remove_client(self, sock):
        address = sock._sock.getpeername()
        self._logger.debug('Removing the connection to (%s, %s).' % address)
        
        self._socket_list.remove(sock)
        self._server_message.remove_player(address)
        
        sock.close()