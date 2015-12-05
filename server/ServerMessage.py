#!/usr/bin/env python

import logging
import SocketServer

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

class ServerMessage(SocketServer.BaseRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ServerMessage')
        self.logger.debug('__init__')
        
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        
        return
    
    def setup(self):
        self.logger.debug('setup')
        
        return SocketServer.BaseRequestHandler.setup(self)
    
    def handle(self):
        self.logger.debug('handle')
        
        # Echo the data back to the client
        data = self.request.recv(1024)
        self.logger.debug('Received: "%s"', data)
        self.request.send(data)
        
        return
    
    def finish(self):
        self.logger.debug('finish')
        
        return SocketServer.BaseRequestHandler.finish(self)