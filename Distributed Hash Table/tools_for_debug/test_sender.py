import os
import sys
import time
import socket
import hashlib
import array








while 1:
    number_of_input = int(input('Number of things to put in: '))
    
    if input('connect?') == 'y':
        port_to_send = input('Port: ')
        return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_port.connect(('127.0.0.1',int(port_to_send)))
        print('connected')
    
    
    
    
    message = ''
    i = 0
    while 1:
        message+= input('Input: ')
        i += 1
        if i == number_of_input:
            break
        else:
            message+='[|Delimiter\\_\\Marker|]'
            
            
    
    return_port.send(message.encode())
            
    i = 0
    message = ''
    