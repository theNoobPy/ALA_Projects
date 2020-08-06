import os
import sys
import time
import socket
import hashlib

#The program stores a Key, Value, Data triplet. The key is a hash generated value while value is assumed to be unique for each entry that is used to identify the entry like say a student number or an email address, data is the data you want to store/lookup in the hash tables.

#Assigns the port used by the client.
try:
    port_for_replies = int(sys.argv[1])
except:
    print("Error parsing supplied argument(S).\nUSAGE: py dht.py 10101")
    sys.exit()

#The hash value generator for the keys
def simple_hash(value):
    
    hashed_val = int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16) % 1000
    
    key = int(hashed_val)
    
    if key <= 100:
        key += 111 #This padds the key values to ensure they have a server to belong to.
    
    return key

#Those with hashed keys starting with n will be stored to server[n-1].
def allocate_keys(num_servers):
    allocation_arr = [] #num_servers = 2: [1,2,1,2,1,2,1,2,1,2] num_servers = 3:[1,2,3,1,2,3,1,2,3,1]
    
    serv_num = 1
    i = 0
    while i < 9:
        allocation_arr.append(serv_num)
        serv_num += 1
        if serv_num > num_servers:
            serv_num = 1
        i += 1
        
    return allocation_arr
    
def listenin(server_name, server_port):
    
    # define socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_name, server_port))
    server_socket.listen(5)
    print('Listening on socket:'+str(server_port))

    conn, address = server_socket.accept() #accept() return the connection object and the address of the client which is why we need 2 variables to store each.
    print('Accepting reply...')
    
    return conn

def which_server(allocation_arr, key):
    search = int(key/100) #note: key will never be 0 as it gets padded if it is below 100
    return allocation_arr[search-1]

#ID giving variables
id_to_give = 0
id_increment_value = 100 #This is 100 because the servers have an array size of 100 in their hash table. The simple_hash function return a 3 digit (XXX) int value greater than 100 like say 170 or 933 so server 1 is responsible for 170 (which it stores in its hash table as key 70) and server 9 is responsible for 933, stored in a similar manner.

def give_id():
    global id_to_give
    id_to_give += id_increment_value
    return id_to_give

# config params for server
def server_conf():
    # lists of (sever name, server port) lists
    server_list = list()
    while 1:
        choice = input('Add a server? [Y/N]: ')
        
        if choice.upper() == 'N':
            break
        if choice.upper() == 'Y':
            server_list.append(('127.0.0.1', int(input('Input Port:'))))
            continue
            
        if choice.upper() == 'D': #debug
            server_list.append(('127.0.0.1', int('10001')))
            server_list.append(('127.0.0.1', int('10002')))
            print('debug command accepted')
            break
            
        print('Invalid Choice')
    
    return server_list


# get command from user
def get_command():
    command = ''
    while 1:
        command = input('Input Command [query, insert, delete, exit]: ')
        if command == 'query' or command == 'insert' or command == 'delete' or command == 'exit':
            return command
            break
        else:
            print('Invalid Command.')
            continue


# define client socket connection
def client():
    # config params for servers
    server_list = server_conf()
    connected = list() #Set to 0 during operation set to 1 during debug
    conns = list()
    port_and_id = list()
    
    for i in range(len(server_list)):
        #Connect to servers specified
        try:
            conns.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            conns[i].connect(server_list[i])
            
            print('Connected to server#'+str(i+1))
            id_assigner = give_id()
            connected.append(conns[i])
            time.sleep(1)
            port_and_id.append([server_list[i],id_assigner])
        except ConnectionRefusedError:
            print('Could not connect to server#', i+1)
            
    #All servers down
    if len(connected) == 0:
        print('No servers are online. System shutting down.')
        sys.exit()
    
    
    #syncronizes all the servers with their neighbors.
    for i in range(0, len(connected)):
        my_command = 'sync'
        comm_message = str(port_for_replies)+'[|Delimiter\\_\\Marker|]'+my_command
        connected[i].send(comm_message.encode())
        
        time.sleep(1)
        
        if len(connected) == 1: #you are the only server
            address, port = port_and_id[0][0]
            neighbor_setter = port
        elif i != (len(connected)-1) and not i > len(connected): #if we have 5 servers and we are assigning the neighbor of say server 4 that will be server 5 but when we get to server 5 we need to realize the neighbor should be server 1
            address, port = port_and_id[i+1][0]
            neighbor_setter = port
        elif i == (len(connected)-1): #this is server 5 that must be synced to server 1
            address, port = port_and_id[0][0]
            neighbor_setter = port
        
        neighbor_and_id = str(neighbor_setter) + '[|Delimiter\\_\\Marker|]' + str(port_and_id[i][1])
        connected[i].send(neighbor_and_id.encode())
        
    allocation_arr = allocate_keys(len(connected))
        
    
    # get command from user -------------------------------
    while 1:
        command = get_command()

        if command == 'insert':
            value = input('Value:')
            key = simple_hash(value)
            data = input('Data:')
            
            comm_message = str(port_for_replies)+'[|Delimiter\\_\\Marker|]'+command
            send_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_port.connect((port_and_id[which_server(allocation_arr, key)-1][0]))
            send_port.send(comm_message.encode())
            
            time.sleep(2)
            message = str(key)+ '[|Delimiter\\_\\Marker|]' + str(value) + '[|Delimiter\\_\\Marker|]' + str(data)
            send_port.send(message.encode())
            listen_to_reply = listenin('127.0.0.1', port_for_replies)
            print(listen_to_reply.recv(2048).decode())
                
        elif command == 'query':
            value = input('Value:')
            key = simple_hash(value)
            
            comm_message = str(port_for_replies)+'[|Delimiter\\_\\Marker|]'+command
            send_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_port.connect((port_and_id[which_server(allocation_arr, key)-1][0]))
            send_port.send(comm_message.encode())
            
            time.sleep(2)
            message = str(key)+ '[|Delimiter\\_\\Marker|]' + str(value)
            send_port.send(message.encode())
            listen_to_reply = listenin('127.0.0.1', port_for_replies)
            print('Query Reply: '+str(listen_to_reply.recv(2048).decode()))
                
        elif command == 'delete':
            value = input('Value:')
            key = simple_hash(value)
            
            comm_message = str(port_for_replies)+'[|Delimiter\\_\\Marker|]'+command
            send_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_port.connect((port_and_id[which_server(allocation_arr, key)-1][0]))
            send_port.send(comm_message.encode())
            
            time.sleep(2)
            message = str(key)+ '[|Delimiter\\_\\Marker|]' + str(value)
            send_port.send(message.encode())
            listen_to_reply = listenin('127.0.0.1', port_for_replies)
            print(listen_to_reply.recv(2048).decode())
                
                
        elif command == 'exit':
            for i in range (0, len(port_and_id)):        
                try:
                    print('Shutting down servers...')
                    comm_message = str(port_for_replies)+'[|Delimiter\\_\\Marker|]'+command
                    send_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    send_port.connect((port_and_id[i][0]))
                    send_port.send(comm_message.encode())
                except:
                    continue #its fine, it just means the server went down before the exit command was given, no big deal.
            print('System shutting down.')
            sys.exit()



# run client
if __name__=='__main__':
    client()