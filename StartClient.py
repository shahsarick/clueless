#!/usr/bin/env python

import logging
import sys
import logging
from client.ClientMessage import ClientMessage
from observer.observer import Observer, observerObject


# Setup logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s: %(message)s')


# Create the client
client_message = ClientMessage()
client_message.start_client()


#TODO: Replace with unit tests and GUI functionality

# create the observer
obsObj = observerObject()
observer = Observer(obsObj.subject)
observer.registerCallback(client_message.receive_message)


while True:
    print 'Waiting for user input.'
    user_input = sys.stdin.readline().rstrip()
    client_message.send_message(user_input)