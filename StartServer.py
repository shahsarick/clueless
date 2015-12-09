#!/usr/bin/env python

import logging
import socket

from server.CluelessServer import CluelessServer

# Setup logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s: %(message)s')

# Create the server
host = socket.gethostbyname(socket.gethostname())
port = 14415
server = CluelessServer(host, port)

# Start the server
server.start_server()