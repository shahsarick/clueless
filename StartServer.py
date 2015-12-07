#!/usr/bin/env python

import socket

from server.CluelessServer import CluelessServer

# Create the server
host = socket.gethostbyname(socket.gethostname())
port = 14415
server = CluelessServer(host, port)

# Start the server
server.start_server()