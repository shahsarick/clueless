#!/usr/bin/env python

import cPickle as pickle
import logging
import socket

from common.Message import Message
from common.MessageEnum import MessageEnum

server_address = ('127.0.0.1', 14415)

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

logger = logging.getLogger('client')

# Connect to the server
logger.debug('Creating socket')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

logger.debug('Connecting to %s on port %s' % server_address)
client_socket.connect(server_address)

# Create message
message = Message(MessageEnum.TURN_BEGIN, 1, 'Beginning turn!')
logger.debug('Sending data: "%s, %s, %s"' % message.get_message_contents())
data_string = pickle.dumps(message)

# Send message
client_socket.sendall(data_string)

# Receive a response
logger.debug('Waiting for response')
data_string = client_socket.recv(1024)
message = pickle.loads(data_string)
logger.debug('Response from server: "%s, %s, %s"' % message.get_message_contents())

# Cleanup
logger.debug('Closing socket')
client_socket.close()
logger.debug('Done')