#!/usr/bin/env python

import sys
import logging
from client.ClientMessage import ClientMessage
from observer.observer import Observer, observerObject

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

client_message = ClientMessage()
client_message.start_client()

# create the observer
obsObj = observerObject()
observer = Observer(obsObj.subject)
observer.registerCallback(client_message.receive_message)

while True:
    print 'Waiting for user input.'
    user_input = sys.stdin.readline().rstrip()
    client_message.send_message(user_input)