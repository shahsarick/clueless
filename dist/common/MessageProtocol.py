#!/usr/bin/env python

import cPickle as pickle
import struct
import time

class MessageProtocol:
    timeout = 0.5
    
    @staticmethod
    def send_msg(sock, message):
        data_string = pickle.dumps(message)
        length = len(data_string)
        
        sock.sendall(struct.pack('!I', length))
        sock.sendall(data_string)
    
    @staticmethod
    def recv_msg(sock):
        length_buffer = MessageProtocol.recvall(sock, 4)
        
        if length_buffer is not None:
            length, = struct.unpack('!I', length_buffer)
            
            data_string = MessageProtocol.recvall(sock, length)
            message = pickle.loads(data_string)
            
            return message, length
        else:
            return '', 0
    
    @staticmethod
    def recvall(sock, count):
        buf = b''
        
        start = time.time()
        
        while count:
            # Check to see if timeout has occurred
            if time.time() - start > MessageProtocol.timeout:
                return None
            
            try:
                new_buffer = sock.recv(count)
                
                if not new_buffer:
                    return None
                
                buf += new_buffer
                count -= len(new_buffer)
            except:
                pass
        
        return buf