#!/usr/bin/env python

import sys

from client.ClientMessage import ClientMessage


client_message = ClientMessage()
client_message.start_client()

while True:
    print 'Waiting for user input.'
    user_input = sys.stdin.readline().rstrip()
    client_message.send_message(user_input)
    client_message.receive_message()