#!/usr/bin/env python

import socket
import sys

from client.Client import Client

host = socket.gethostbyname(socket.gethostname())
port = 14415

client = Client(host, port)
client.initialize()

while True:
    print 'Waiting for user input.'
    user_input = sys.stdin.readline().rstrip()
    client.send_message(user_input)