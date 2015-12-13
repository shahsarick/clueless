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
def suggest():
    pass
def accuse():
    pass
def move():
    room = prompt_move()
    #TODO: Gameboard needs to be updated with new positions
    if room != -1:
        message_args = [room]
        message = Message(MessageEnum.MOVE, 1, message_args)
        client_message.send_message(message)
    else:
        print 'Invalid room number'
def turn_over():
    message = Message(MessageEnum.TURN_OVER, 1, [True])
    client_message.send_message(message)

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
        client_message.return_client_model_instance().has_moved = True
        sleep(3)
        while client_message.return_client_model_instance().must_suggest == True:
            print "you must suggest"
            player_input = sys.stdin.readline().rstrip()
            if player_input =='suggest':
                client_message.return_client_model_instance().must_suggest = False
                suggest()
                client_message.return_client_model_instance().has_suggested = True

    elif player_input == 'over':
        turn_over()
        #reset what the client can do/has done
        client_message.return_client_model_instance().reset_all()
        sleep(3)
    elif player_input == 'accuse':
        # you can only accuse once
        client_message.return_client_model_instance().has_accused = True
        accuse()
        sleep(3)
    else:
        print "command not recognized"
