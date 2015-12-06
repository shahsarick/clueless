#!/usr/bin/env python

from server.CluelessServer import CluelessServer

# Create the server
host = '127.0.0.1'
port = 14415
server = CluelessServer(host, port)

# Start the server
server.start_server()