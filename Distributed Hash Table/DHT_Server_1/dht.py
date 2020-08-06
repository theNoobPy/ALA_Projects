import os
import sys
import time
import socket
import hashlib
import array

#Implementation details:
#https://www.youtube.com/watch?v=KyUTuwz_b7Q
#Title of Video: Hash Tables and Hash Functions
#Channel: Computer Science
#Essentially Key is the hashed version of Value which determines it place on the table, Value is the Value to look up, and Data is the important data you are trying to look up.

class Key_N_Data:
    def __init__(self, Key, Value, Data):
        self.Key = Key
        self.Value = Value
        self.Data = Data

HT_SIZE_LIMIT = 100
class Hash_Table:
    neighbor = 0 #this is the address and port number tuple of the neighbor
    neighbor_checker = 0 #this is port only
    ht_id = 0
    Table = ['empty'] * HT_SIZE_LIMIT
    
    def __init__(self, neighbor, ht_id):
        self.neighbor = ('127.0.0.1', int(neighbor))
        self.ht_id = ht_id
        self.neighbor_checker = neighbor
        
        #makes the array populated with empty Key_N_Data objects
        i = 0
        while i < HT_SIZE_LIMIT:
            n = Key_N_Data(i,'','')
            self.Table[i] = n
            i += 1
    
    #simple linear insert onto the hash table
    def ins_tab(self, add_me):
        test_key = int(add_me.Key)
        maybe_full = 0
        

        
        while 1:
        
            if test_key >= HT_SIZE_LIMIT:
                if not maybe_full:
                    test_key = 0
                    maybe_full = 1
                else:
                    return('Error: table is full')
                    
                    
            if self.Table[test_key].Data == '':
                self.Table[test_key] = add_me
                return('Success')
                
            
            test_key += 1
            
            
    
    #simple linear search
    def query(self, key, value):
        search = int(key)
        maybe_not_here = 0
        

        
        while 1:
            
            if search >= HT_SIZE_LIMIT:
                if not maybe_not_here:
                    maybe_not_here = 1
                    search = 0
                else:
                    return('Error: value not found')
            
            
            
            if value == self.Table[search].Value:
                return self.Table[search]
                
            search += 1
            
                    
                    
                    
    #simple linear search for deletion
    def delete(self, key, value):
        search = int(key)
        maybe_not_here = 0
        

        
        while 1:
        
            if search >= HT_SIZE_LIMIT:
                if not maybe_not_here:
                    maybe_not_here = 1
                    search = 0
                else:
                    return('Error: value not found')

            
            
            if value == self.Table[search].Value:
                n = Key_N_Data(search,'','')
                self.Table[search] = n
                return('Success')
                break
                
            search += 1
            

# function to check port number assignment
def check_args():

    # error handling argument
    if len(sys.argv) != 2:
        print("Please supply port number.\nUSAGE: py dht.py 10001")
        sys.exit()

    # error handling port number 
    else:
        try:
            return int(sys.argv[1])
        except ValueError:
                print("Error parsing supplied argument(S).")
                sys.exit()

# query the indicated table for the key value pair
def query_table(communication):
    received = communication[3].recv(2048).decode()
    key, value = received.split('[|Delimiter\\_\\Marker|]')
    communication[3].close()

    try:
        print ('Query for Key '+str(key)+' Value '+str(value))
        reply = str(ht.query(key, value).Data)
        
        print(reply)
        
        return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_port.connect(communication[1])
        return_port.send(reply.encode())
        return_port.close()
        
    except:
        print('Not found, sending to neighbor')
        
        if ht.neighbor_checker == sys.argv[1]:
            print('Have no neighbor')
            reply = 'Not found'
            return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return_port.connect(communication[1])
            return_port.send(reply.encode())
            return_port.close()
            return
            
        communication_address, communication_port = communication[1]
        
        neighbor_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_port.connect(ht.neighbor)
        command_to_neighbor = str(communication_port)+'[|Delimiter\\_\\Marker|]'+'query_neighbor'
        neighbor_port.send(command_to_neighbor.encode())
        
        
        print('awaiting ready')
        neighbor_port.recv(2048)
        message_string = key+'[|Delimiter\\_\\Marker|]'+value+'[|Delimiter\\_\\Marker|]'+sys.argv[1]+'[|Delimiter\\_\\Marker|]'+communication_address+'[|Delimiter\\_\\Marker|]'+str(communication_port)
        neighbor_port.send(message_string.encode())
        neighbor_port.close()
        
# function to recieve the query from synced neighbor
def query_neighbor(conn):
    ready_string = 'ready'
    conn.send(ready_string.encode())
    received = conn.recv(2048).decode()
    key, value, sender, reply_address, reply_port = received.split('[|Delimiter\\_\\Marker|]')



    try:
        print ('Query for Key '+str(key)+' Value '+str(value))

        reply = str(ht.query(key, value).Data)
        
        print(reply)
        
        return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_port.connect((reply_address,int(reply_port)))
        return_port.send(reply.encode())
        return_port.close()
        
    except:
        if sender == ht.neighbor_checker: #my neighbor, the one I am going to query, is the one that propagated the request originally. Therefore, I should just end the process because he didn't have it and neither did the entire circle.
            reply = 'Not found'
            print(reply)
            return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return_port.connect((reply_address, int(reply_port)))
            return_port.send(reply.encode())
            return_port.close()
            return
    
        print('Not found, sending to neighbor')
        neighbor_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_port.connect(ht.neighbor)
        command_to_neighbor = reply_port+'[|Delimiter\\_\\Marker|]'+'query_neighbor'
        neighbor_port.send(command_to_neighbor.encode())
        
        print('awaiting ready')
        neighbor_port.recv(2048)
        message_string = key+'[|Delimiter\\_\\Marker|]'+value+'[|Delimiter\\_\\Marker|]'+sender+'[|Delimiter\\_\\Marker|]'+reply_address+'[|Delimiter\\_\\Marker|]'+reply_port
        neighbor_port.send(message_string.encode())
        neighbor_port.close()

#insert section
def insert_key(communication):
    received = communication[3].recv(2048).decode()
    key, value, data = received.split('[|Delimiter\\_\\Marker|]')
    communication[3].close()

    try:
        print ('Attempting to insert Key '+str(key)+' Value '+str(value))
        
        insert_me = Key_N_Data(key,value,data)
        reply = ht.ins_tab(insert_me)
        print(reply)
        
        if reply != 'Success':
            assert 1 == 0
            
        
        return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_port.connect(communication[1])
        return_port.send(reply.encode())
        return_port.close()
        
        
        
    except:
        print('Table is full, sending to neighbor')
        
        if ht.neighbor_checker == sys.argv[1]:
            print('Have no neighbor')
            reply = 'Not found'
            return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return_port.connect(communication[1])
            return_port.send(reply.encode())
            return_port.close()
            return
        
        communication_address, communication_port = communication[1]
        
        neighbor_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_port.connect(ht.neighbor)
        command_to_neighbor = str(communication_port)+'[|Delimiter\\_\\Marker|]'+'insert_neighbor'
        neighbor_port.send(command_to_neighbor.encode())
        
        
        print('awaiting ready')
        neighbor_port.recv(2048)
        message_string = key+'[|Delimiter\\_\\Marker|]'+value+'[|Delimiter\\_\\Marker|]'+data+'[|Delimiter\\_\\Marker|]'+sys.argv[1]+'[|Delimiter\\_\\Marker|]'+ communication_address + '[|Delimiter\\_\\Marker|]' + str(communication_port)
        neighbor_port.send(message_string.encode())
        neighbor_port.close()
        
        
    
def insert_neighbor(conn):
    ready_string = 'ready'
    conn.send(ready_string.encode())
    received = conn.recv(2048).decode()
    key, value, data, sender, reply_address, reply_port = received.split('[|Delimiter\\_\\Marker|]')
    

    try:
        print ('Attempting to insert Key '+str(key)+' Value '+str(value))

        insert_me = Key_N_Data(key,value,data)
        reply = ht.ins_tab(insert_me)
        
        print(reply)
        
        if reply != 'Success':
            assert 1 == 0
        
        return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_port.connect((reply_address, int(reply_port)))
        return_port.send(reply.encode())
        return_port.close()
        
    except:
    
        if sender == ht.neighbor_checker: #my neighbor, the one I am going to ask to insert, is the one that propagated the request originally. Therefore, I should just end the process because it is full, I am full, and the entire circle is full.
            reply = 'All tables are full'
            print(reply)
            return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return_port.connect((reply_address, int(reply_port)))
            return_port.send(reply.encode())
            return_port.close()
            return
    
        print('Table is full, sending to neighbor')
        neighbor_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_port.connect(ht.neighbor)
        command_to_neighbor = reply_port+'[|Delimiter\\_\\Marker|]'+'insert_neighbor'
        neighbor_port.send(command_to_neighbor.encode())
        
        print('awaiting ready')
        neighbor_port.recv(2048)
        message_string = key+'[|Delimiter\\_\\Marker|]'+value+'[|Delimiter\\_\\Marker|]'+data+'[|Delimiter\\_\\Marker|]'+sender+'[|Delimiter\\_\\Marker|]'+reply_address+'[|Delimiter\\_\\Marker|]'+reply_port
        neighbor_port.send(message_string.encode())
        neighbor_port.close()

#delete key section

def delete_key(communication):
    received = communication[3].recv(2048).decode()
    key, value = received.split('[|Delimiter\\_\\Marker|]')
    communication[3].close()

    try:
        print ('Attempting to delete Key '+str(key)+' Value '+str(value))
        
        reply = ht.delete(key,value)
        print(reply)
        
        if reply != 'Success':
            assert 1 == 0
            
        
        return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_port.connect(communication[1])
        return_port.send(reply.encode())
        return_port.close()
        
        
        
    except:
        print('Not found, sending to neighbor')
        
        if ht.neighbor_checker == sys.argv[1]:
            print('Have no neighbor')
            reply = 'Not found'
            return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return_port.connect(communication[1])
            return_port.send(reply.encode())
            return_port.close()
            return
        communication_address, communication_port = communication[1]
        
        neighbor_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_port.connect(ht.neighbor)
        command_to_neighbor = str(communication_port)+'[|Delimiter\\_\\Marker|]'+'delete_key_neighbor'
        neighbor_port.send(command_to_neighbor.encode())
        
        
        print('awaiting ready')
        neighbor_port.recv(2048)
        message_string = key+'[|Delimiter\\_\\Marker|]'+value+'[|Delimiter\\_\\Marker|]'+sys.argv[1]+'[|Delimiter\\_\\Marker|]'+communication_address+'[|Delimiter\\_\\Marker|]'+str(communication_port)
        neighbor_port.send(message_string.encode())
        neighbor_port.close()
        
        
    
def delete_key_neighbor(conn):
    ready_string = 'ready'
    conn.send(ready_string.encode())
    received = conn.recv(2048).decode()
    key, value, sender, reply_address, reply_port = received.split('[|Delimiter\\_\\Marker|]')
    


    try:
        print ('Attempting to delete Key '+str(key)+' Value '+str(value))

        reply = ht.delete(key, value)
        
        print(reply)
        
        if reply != 'Success':
            assert 1 == 0
        
        return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_port.connect((reply_address,int(reply_port)))
        return_port.send(reply.encode())
        return_port.close()
        
    except:
    
        if sender == ht.neighbor_checker: #my neighbor, the one I am going to ask to insert, is the one that propagated the request originally. Therefore, I should just end the process because it is full, I am full, and the entire circle is full.
            reply = 'Not found'
            print(reply)
            return_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return_port.connect((reply_address, int(reply_port)))
            return_port.send(reply.encode())
            return_port.close()
            return
    
        print('Not found, sending to neighbor')
        neighbor_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        neighbor_port.connect(ht.neighbor)
        command_to_neighbor = reply_port+'[|Delimiter\\_\\Marker|]'+'delete_key_neighbor'
        neighbor_port.send(command_to_neighbor.encode())
        
        print('awaiting ready')
        neighbor_port.recv(2048)
        message_string = key+'[|Delimiter\\_\\Marker|]'+value+'[|Delimiter\\_\\Marker|]'+'[|Delimiter\\_\\Marker|]'+sender+'[|Delimiter\\_\\Marker|]'+reply_address+'[|Delimiter\\_\\Marker|]'+reply_port
        neighbor_port.send(message_string.encode())
        neighbor_port.close()
    
    
#
def query_id(conn):
    conn.send(ht.ht_id.encode())
    conn.close()
    
    
ht = 0 #set the hash table to be global.
# sync with neighbor, hence sync_n
def sync_n(conn):
    print('Sync initiated')
    print('Awaiting for input (neighbor, id)')
    neighbor_conn = conn.recv(1024).decode()
    ht_neighbor, ht_id = neighbor_conn.split('[|Delimiter\\_\\Marker|]')
    print('Sync with neighbor '+str(neighbor_conn) + '\nAssigning ID:' + str(ht_id))
    global ht
    ht = Hash_Table(ht_neighbor, ht_id) #creates the hash table and sets its neighbor.
    print('Success')
    conn.close()
    
    
   
def listen(server_name, server_port):
    
    # define socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_name, server_port))
    server_socket.listen(5)
    print('Server listening on socket:'+str(server_port))

    conn, address = server_socket.accept() #accept() return the connection object and the address of the client which is why we need 2 variables to store each.
    print('Connected to Client.')
    
    
    print('awaiting ready')
    received = conn.recv(2048).decode()
    print('Comms recieved: ' +received + ' recieved.')
    port, command = received.split('[|Delimiter\\_\\Marker|]')
    
    port = ('127.0.0.1', int(port))
    
    listen_arr = [address, port, command, conn] #remember to close the connection after each function.
    
    return listen_arr



def control():
    server_name = '127.0.0.1'
    server_port = int(sys.argv[1])

    while 1:
        
        #calls the function to recieve commands from the client
        communication = listen(server_name, server_port)
    
    
        # address  - 0, port - 1, command - 2, conn - 3
        command = communication[2] #this extra memory/variable is used for the sake of clarity.

            
        # Sync with neighbor
        if command == 'sync':
            sync_n(communication[3])

        # Query
        elif command == 'query':
            query_table(communication)
            
        # Passed on
        elif command == 'query_neighbor':
            query_neighbor(communication[3])

        # Insert key into table
        elif command == 'insert':
            insert_key(communication)
            
        # Insert key into neighbor
        elif command == 'insert_neighbor':
            insert_neighbor(communication[3])

        # delete key
        elif command == 'delete':
            delete_key(communication)
            
        # delete key from neighbor
        elif command == 'delete_key_neighbor':
            delete_key_neighbor(communication[3])
            
        # queries the id of the hash table. note: this is not used by the client code as the current client code keeps its own array that tells it which port has which hash table id because the current implementation is single client due to the troubles of having race conditions when we have multiple clients, this is here in case someone wants to use this server code with a different client code that is able to handle the race issues of multiple clients.
        elif command == 'query_id':
            query_id(conn)

        # Exit
        elif command == 'exit':
            print('User requested to exit. Server shutting down.')
            break

        # handle wrong command
        else:
            print('Command does not exist.') #here we are assuming something catastrophic happened such as a race condition, to avoid the program just freezing there waiting for a response that will likely never come, we just exit.
            sys.exit()


    sys.exit()

  
if __name__=='__main__':

    check_args()
    control()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    