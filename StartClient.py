#!/usr/bin/env python

import logging
import socket
import sys

from client.ClientMessage import ClientMessage

from common.Message import Message
from common.MessageEnum import MessageEnum

from observer.observer import Observer, observerObject

#TODO: Move all relevant code to GUI

# Setup logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)d | %(levelname)s | %(module)s.%(funcName)s : %(message)s', datefmt="%H:%M:%S")

def add_lobby():
    print 'Please enter your username'
    username = sys.stdin.readline().rstrip()
    
    message_args = [username]
    message = Message(MessageEnum.LOBBY_ADD, 1, message_args)
    client_message.send_message(message)

# Create the client
#TODO: Get IP from GUi
host = socket.gethostbyname(socket.gethostname())
port = 14415

client_message = ClientMessage()
connected = client_message.connect_to_server(host, port)

# Create the observer
if connected == True:
    obsObj = observerObject()
    observer = Observer(obsObj.subject)
    observer.registerCallback(client_message.handle_message)
    
    add_lobby()
else:
    print 'Failed to connect with server.'