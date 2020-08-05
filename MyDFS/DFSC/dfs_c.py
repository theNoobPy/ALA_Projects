import os
import sys
import time
import socket
from send2trash import send2trash #remember to get this installed via pip/cuda install Send2Trash

#Split Functions
def split(fromfile, todir, chunksize): 
    if not os.path.exists(todir):                  # check if the path isn't created yet
        os.mkdir(todir)                            # make creates the path if it is not
    else:
        for fname in os.listdir(todir):            # delete any existing files, be very careful here
            send2trash(os.path.join(todir, fname)) 
    partnum = 0
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        assert partnum <= 9999                     # join sort fails if there are too many parts.
        filename = os.path.join(todir, ('part'+str(partnum)))
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close(  )
    
    return partnum
    
def allocate_parts(parts, buckets): 
    parts_list = range(1, parts+1)
    butckest_a = []
    allocated = 0
    allocator = 0
    
    for i in range(0, buckets):
        sub_list = []
        butckest_a.append(sub_list)
    
    for i in range(0, parts):
        if allocated == len(parts_list):
            break
        else:
            #print('assigning i = '+str(i)+' to '+str(allocator)) #debug lines
            #print (parts_list[i])                                #debug lines
            #print (butckest_a[allocator])                        #debug lines
            butckest_a[allocator].append(parts_list[i])
            allocator += 1
            if allocator == buckets:
                allocator = 0
            allocated += 1
        
    return butckest_a

#function to build the file from the downloaded parts
def join_file(fromdir, tofile):
    output = open(tofile, 'wb')
    parts  = os.listdir(fromdir)
    parts.sort(  )
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj  = open(filepath, 'rb')
        while 1:
            filebytes = fileobj.read(1024)
            if not filebytes: break
            output.write(filebytes)
        fileobj.close(  )
    output.close(  )
    send2trash(fromdir)
    

# config params for server
def server_conf():
    # lists of (sever name, server port) lists
    global server_list
    server_list = list()
    while 1:
        choice = input('Add a server? [Y/N]: ')
        
        if choice.upper() == 'N':
            break
        if choice.upper() == 'Y':
            server_list.append((input('Input IP address:'), int(input('Input Port:'))))
            continue
        print('Invalid Choice')
    
    return server_list



# get command from user
def get_command():
    command = ''
    while 1:
        command = input('Input Command [list, get, put, exit]: ')
        if command == 'list' or command == 'get' or command == 'put' or command == 'exit':
            return command
            break
        else:
            print('Invalid Command.')
            continue



    
# define client socket connection
def client():
    # config params for servers
    server_list = server_conf()
    connected = 0 #Set to 0 during operation set to 1 during debug
    conns = list()
    
    for i in range(len(server_list)):
        #Connect to servers specified
        try:
            conns.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            conns[i].connect(server_list[i])
            status_s = ('Connected to server#', str(i+1))
            print(status_s[0], status_s[1])
            connected += 1
            time.sleep(1)
        except ConnectionRefusedError:
            print('Could not connect to server#', i+1)
    
    
        
    #All servers down
    if connected == 0:
        print('No servers are online. System shutting down.')
        sys.exit()
        
    
    #send username
    username = input('Enter username: ')
    if not os.path.exists(username):                  # check if the path isn't created yet
        os.mkdir(username)                            # make dir creates the path if it is not
    
    try:
        for i in range(len(conns)):
            conns[i].send(username.encode())
    except OSError:
        pass
    
    # get command from user -------------------------------
    while 1:
        command = get_command()
    
        #send command to server
        try:
            for i in range(len(conns)):
                conns[i].send(command.encode())
        except OSError:
            pass



        if command == 'list':
            for i in range(len(conns)):        
                try:
                    file_names=conns[i].recv(4096).decode()
                    # print a table for each server 
                    print('\nServer#' +str(i+1) + ' ' + username +' files:')
                    print(file_names)
                except OSError:
                    pass
                    
                    
                    
        elif command == 'put':
                file_name = input('Enter Filename: ')
                n = 2 #the defult number of parts to split the file. If the size in bytes isn't quite divisible by 2 it will generate 3 parts.
                
                
                chunksize = int(os.stat(file_name).st_size/(n*connected)) #determines how large each part is based on the number of connected servers, e.g. 1 server:2-3 parts, 2 servers:4-5 parts with each server hosting 2 parts (or a 3-2 split if its 5 parts)
                todir = os.getcwd()+'\\'+username+'\\'+file_name
                if not os.path.exists(todir):                  # check if the path isn't created yet
                    os.mkdir(todir)                            # make dir creates the path if it is not
                
                try:
                    parts = split(file_name, todir, chunksize)
                except Exception as e:
                    print ('Error during split')
                    print (e)
                else:
                    print ('Split finished:', parts, 'parts are in', todir)
                
                #print(len(os.listdir(todir)))                             #debug line that shows how many files are in the folder
                
                allocated_parts = allocate_parts(len(os.listdir(todir)), connected)
                
                print('Starting transfer...')
                #print(allocated_parts)                                    #debug line to show the allocation
                
                command = file_name
                for i in range(0,connected):
                    conns[i].send(command.encode())
                
                for i in range(0,connected):
                    for j in allocated_parts[i]:
                        file_to_send = todir+'\\'+'part'+str(j)
                        print('Sending:'+file_to_send+' of size '+str(os.stat(file_to_send).st_size)+'KB to server#'+str(i+1))
                        
                        if j == allocated_parts[i][len(allocated_parts[i])-1]:
                            send_another_file = 0
                        else:
                            send_another_file = 1
                        
                        command = str(j)+'[|Delimiter\\_\\Marker|]'+str(os.stat(file_to_send).st_size)+'[|Delimiter\\_\\Marker|]'+str(send_another_file)#the delim marker has \s cause those aren't allowed on file names making it a reliable delimiter.
                        conns[i].send(command.encode())
                        
                        f = open(file_to_send,'rb')
                        l = f.read(int(os.stat(file_to_send).st_size))
                        time.sleep(1)
                        conns[i].send(l)
                        f.close()
                        
                        wait_for_complete = conns[i].recv(1024).decode()
                        print(wait_for_complete)
                
                print('Transfer Complete')
                send2trash(todir)
                send2trash(file_name)
                
        elif command == 'get':
                file_name = input('Enter Filename: (enter the name of the file without \"part\") ')
                store_directory = os.getcwd()+'\\'+username+'\\'+file_name
                if not os.path.exists(store_directory):                  # check if the path isn't created yet
                    os.mkdir(store_directory)                            # make dir creates the path if it is not
                
                
                for i in range(0,connected):
                    conns[i].send(file_name.encode())
                    while 1:
                        received = conns[i].recv(2048).decode()
                        part_name, part_size, another_one = received.split('[|Delimiter\\_\\Marker|]')
                        print('Accepting:'+str(part_name)+' of size '+str(part_size))
                        try:
                            f = open(str(store_directory)+ '\\' + str(part_name),'wb') 
                            
                            l = conns[i].recv(int(part_size))
                            f.write(l)
                            f.close()
            
                            time.sleep(1)
                            print('Done writing file: ' + store_directory+ '\\' + str(part_name))
                            reply = 'CLIENT REPLY: OK'
                            conns[i].send(reply.encode())
                        except Exception as e:
                            print('An error has occured')
                            print(e)
                            reply = 'CLIENT REPLY: FAILED_TO_WRITE_FILE'
                            conns[i].send(reply.encode())
                            continue
                        
                        if another_one == '0':
                            break
                    
                    
                
                print('Transfer Complete')
                join_file(store_directory, file_name)
                
                
        elif command == 'exit':
            print('Shutting down.')
            sys.exit()



# run client
if __name__=='__main__':
    client()