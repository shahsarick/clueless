#!/usr/bin/env python

import logging
import socket

server_address = ('127.0.0.1', 14415)

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

logger = logging.getLogger('client')

# Connect to the server
logger.debug('Creating socket')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

logger.debug('Connecting to %s on port %s' % server_address)
client_socket.connect(server_address)

# Send data
message = 'This is my test message'
logger.debug('Sending data: "%s"', message)
client_socket.sendall(message)

# Receive a response
logger.debug('Waiting for response')
response = client_socket.recv(1024)
logger.debug('Response from server: "%s"', response)

# Cleanup
logger.debug('Closing socket')
client_socket.close()
logger.debug('Done')