import os
import sys
import time
import socket
import hashlib
import array



def listenin(server_name, server_port):
    
    # define socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_name, server_port))
    server_socket.listen(5)
    print('Listening on socket:'+str(server_port))

    conn, address = server_socket.accept() #accept() return the connection object and the address of the client which is why we need 2 variables to store each.
    print('Reply Accepted.')
    
    
    return conn

while input('again? ') != 'n':
    arr = listenin('127.0.0.1', 10101)
    print(arr.recv(2048).decode())
    
    








