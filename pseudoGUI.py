__author__ = 'Stephen Bailey'
#!/usr/bin/env python

import logging
import socket
import sys
from client.ClientMessage import ClientMessage
from common.Message import Message
from common.MessageEnum import MessageEnum
from observer.observer import Observer, observerObject
from time import sleep

#TODO: Move all relevant code to GUI

# Setup logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)d | %(levelname)s | %(module)s.%(funcName)s : %(message)s', datefmt="%H:%M:%S")

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
else:
    print 'Failed to connect with server.'
sleep(2)



message_args = None
# GUI methods
def promptUserName():
    print 'Please enter your username'
    username = sys.stdin.readline().rstrip()
    global message_args
    message_args = [username]
    return [username]

def add_lobby():
    message_args = promptUserName()
    message = Message(MessageEnum.LOBBY_ADD, 1, message_args)
    client_message.send_message(message)

def lobby_ready():
    message = Message(MessageEnum.LOBBY_READY, 1, [True])
    client_message.send_message(message)

def lobby_unready():
    message = Message(MessageEnum.LOBBY_UNREADY, 1, [False])
    client_message.send_message(message)


#loop to simulate GUI actions
while True:
    print "Enter a command: "
    playerInput = sys.stdin.readline().rstrip()

    if playerInput == "lobby add":
        add_lobby()
        sleep(2)
    elif playerInput == "lobby ready":
        lobby_ready()
        sleep(2)
    elif playerInput == "lobby unready":
        lobby_unready()
        sleep(2)
    else:
        print "command not recognized"
