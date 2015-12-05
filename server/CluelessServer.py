#!/usr/bin/env python

import logging
import SocketServer

import ServerMessage

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

class CluelessServer(SocketServer.TCPServer):

    def __init__(self, host, port, handler_class=ServerMessage):
        self.logger = logging.getLogger('CluelessServer')
        self.logger.debug('__init__')
        
        self.server_address = (host, port)
        
        SocketServer.TCPServer.__init__(self, self.server_address, handler_class)
        
        return
    
    def server_activate(self):
        self.logger.debug('server_activate')
        
        SocketServer.TCPServer.server_activate(self)
        
        return
    
    def serve_forever(self):
        self.logger.debug('serve_forever')
        self.logger.info('Handling requests, press <Ctrl-Pause/Break or Ctrl-C> to quit')
        
        while True:
            self.handle_request()
        
        return
    
    def handle_request(self):
        self.logger.debug('handle_request')
        
        return SocketServer.TCPServer.handle_request(self)
    
    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        
        return SocketServer.TCPServer.verify_request(self, request, client_address)
    
    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)', request, client_address)
        
        return SocketServer.TCPServer.process_request(self, request, client_address)
    
    def server_close(self):
        self.logger.debug('server_close')
        
        return SocketServer.TCPServer.server_close(self)
    
    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)', request, client_address)
        
        return SocketServer.TCPServer.finish_request(self, request, client_address)
    
    def close_request(self, request):
        self.logger.debug('close_request(%s)', request)
        
        return SocketServer.TCPServer.close_request(self, request)