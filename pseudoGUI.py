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
    print 'Please enter the player_enum'
    player_enum = int(sys.stdin.readline().rstrip())
    
    print 'Please enter the weapon_enum'
    weapon_enum = int(sys.stdin.readline().rstrip())
    
    current_room = client_message.return_client_model_instance().get_character_position()
    
    message_args = [player_enum, weapon_enum, current_room]
    message = Message(MessageEnum.SUGGESTION_BEGIN, 1, message_args)
    client_message.send_message(message)

def disprove():
    player_enum_list, weapon_list, room_list = client_message.get_cards()
    suggestion = client_message.get_suggestion()
    
    matched_player_enum = False
    matched_weapon = False
    matched_room = False
    
    for player_enum in player_enum_list:
        if player_enum == suggestion[0]:
            print "Suggestion matches your player_enum"
            
            matched_player_enum = True
            break
    
    for weapon in weapon_list:
        if weapon == suggestion[1]:
            print "Suggestion matches your weapon"
            
            matched_weapon = True
            break
    
    for room in room_list:
        if room == suggestion[2]:
            print "Suggestion matches your room"
            
            matched_room = True
            break
    
    message_args = [None, None, None]
    
    if matched_player_enum == True or matched_weapon == True or matched_room == True:
        matched = False
        
        while matched == False:
            print 'Type 1 to show player, 2 to show weapon, or 3 to show room'
            
            choice = int(sys.stdin.readline().rstrip())
            
            if choice == 1 and matched_player_enum == True:
                matched = True
                message_args[0] = player_enum
            elif choice == 2 and matched_weapon == True:
                matched = True
                message_args[1] = weapon
            elif choice == 3 and matched_room == True:
                matched = True
                message_args[2] = room
    
    message = Message(MessageEnum.SUGGEST, 1, message_args)
    client_message.send_message(message)

def accuse():
    print 'Enter the player_enum to accuse'
    player_enum = int(sys.stdin.readline().rstrip())
    print 'Enter the weapon_enum to accuse'
    weapon_enum = int(sys.stdin.readline().rstrip())
    print 'Enter the room_enum to accuse'
    room_enum = int(sys.stdin.readline().rstrip())
    message_args=[player_enum, weapon_enum, room_enum]
    message = Message(MessageEnum.ACCUSE, 1, message_args)
    client_message.send_message(message)

def move():
    room = prompt_move()
    
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
    # player can take no more actions if they have already accused
    if client_message.return_client_model_instance()._has_accused == False:
        if player_input == "lobby ready":
            lobby_ready()
            sleep(3)
        elif player_input == "lobby unready":
            lobby_unready()
            sleep(3)
        elif player_input == 'move':
            move()
            sleep(6)
            while client_message.need_suggestion() == True:
                print "Type suggest to make a suggestion."

                player_input = sys.stdin.readline().rstrip()

                if player_input == 'suggest':
                    client_message.make_suggestion()
                    suggest()

        elif player_input == 'disprove':
            disprove()
        elif player_input == 'over':
            turn_over()
            #reset what the client can do/has done
            client_message.return_client_model_instance().reset_all()
            sleep(3)
        elif player_input == 'accuse':
            # you can only accuse once
            client_message.return_client_model_instance()._has_accused = True
            accuse()
            sleep(3)

        elif player_input == 'suggest':
            client_message.make_suggestion()
            suggest()

        else:
            print "command not recognized"

    else:
        print "You have already accused, you may take no more actions."
