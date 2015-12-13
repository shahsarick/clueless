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

# GUI methods
def prompt_move():
    print 'Please enter a room number to move to (see RoomEnum.py)'
    
    try:
        room = int(sys.stdin.readline().rstrip())
        return room
    except ValueError:
        return -1

def lobby_ready():
    message = Message(MessageEnum.LOBBY_READY, 1, [True])
    client_message.send_message(message)

def lobby_unready():
    message = Message(MessageEnum.LOBBY_UNREADY, 1, [False])
    client_message.send_message(message)

def move():
    room = prompt_move()
    
    if room != -1:
        message_args = [room]
        message = Message(MessageEnum.MOVE, 1, message_args)
        client_message.send_message(message)
    else:
        print 'Invalid room number'

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

#loop to simulate GUI actions
while True:
    print "Enter a command: "
    player_input = sys.stdin.readline().rstrip()

    if player_input == "lobby ready":
        lobby_ready()
        sleep(3)
    elif player_input == "lobby unready":
        lobby_unready()
        sleep(3)
    elif player_input == 'move':
        move()
        sleep(3)
    else:
        print "command not recognized"
