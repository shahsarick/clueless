#!/usr/bin/env python

import threading

from server.CluelessServer import CluelessServer
from server.ServerMessage import ServerMessage

# Create the server
host = '127.0.0.1'
port = 14415
server = CluelessServer(host, port, ServerMessage)

# Create server daemon
server_thread = threading.Thread(target=server.serve_forever())
server_thread.setDaemon(True)
server_thread.start()