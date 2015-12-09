#!/usr/bin/env python

import logging
import socket

from server.CluelessServer import CluelessServer

# Setup logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)d | %(levelname)s | %(module)s.%(funcName)s : %(message)s', datefmt="%H:%M:%S")

# Create the server
host = socket.gethostbyname(socket.gethostname())
port = 14415
server = CluelessServer(host, port)

# Start the server
server.start_server()