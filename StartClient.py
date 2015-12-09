#!/usr/bin/env python

import logging
import sys

from client.ClientMessage import ClientMessage

# Setup logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)d | %(levelname)s | %(module)s.%(funcName)s : %(message)s', datefmt="%H:%M:%S")

# Create the client
client_message = ClientMessage()
client_message.start_client()

#TODO: Replace with unit tests and GUI functionality
while True:
    print 'Waiting for user input.'
    user_input = sys.stdin.readline().rstrip()
    client_message.send_message(user_input)