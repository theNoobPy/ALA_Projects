import os
import sys
import time
import socket

# function to check port number assignment
def check_args():

    # error handling argument
    if len(sys.argv) != 2:
        print("Please supply port number.\nUSAGE: py dfs1.py 10001")
        sys.exit()

    # error handling port number 
    else:
        try:
            return int(sys.argv[1])
        except ValueError:
                print("Error parsing supplied argument(S).")
                sys.exit()

# put files into servers
def put(new_dir_path):
    print('Prepared to receive.')
    
    file_name = conn.recv(2048).decode()
    savepath = new_dir_path+'\\'+file_name
    if not os.path.exists(savepath):                  # check if the path isn't created yet
        os.mkdir(savepath)                            # make creates the path if it is not
    
    while 1:
        received = conn.recv(2048).decode()
        part, part_size, another_one = received.split('[|Delimiter\\_\\Marker|]')
        print('accepting part'+str(part)+' of size '+str(part_size))
        
        try:
            f = open(str(savepath)+ '\\' + str(file_name) + 'part' + str(part),'wb') 
            
            
            l = conn.recv(int(part_size))
            f.write(l)
            f.close()
            
            time.sleep(1)
            print('Done writing file: ' + str(savepath) + '\\' + str(file_name) + 'part' + str(part))
            reply = 'SERVER REPLY: OK'
            conn.send(reply.encode())
        except Exception as e:
            print('An error has occured')
            print(e)
            reply = 'SERVER REPLY: FAILED_TO_WRITE_FILE'
            conn.send(reply.encode())
            continue
        
        
        if another_one == '0':
            break
    
    


# creates new directory for user
def new_dir(username):
    # define new path
    global new_dir_path
    new_dir_path = os.getcwd() +'\\' +username

    # if path does not exist, create new dir 
    if os.path.isdir(new_dir_path) == False:
        try:  
            os.mkdir(new_dir_path)
            print ("Successfully created the directory " + new_dir_path)    
            return new_dir_path
        except:
            print ("Creation of the directory "+new_dir_path+" failed")
    
    # return the dir path if exists
    else:
        return new_dir_path

# command to list files in servers    
def list_files(username):

    # get list of files from subdirectory   
    user_dir = os.getcwd() +'\\' +username
    file_dir_list = next(os.walk(user_dir))[1]
    
    # if user has no file directory (has never sent files)
    if file_dir_list == []:
        response='There is no directory for the user.'
        print(response)
        conn.send(response.encode())
        
    else:
        # start a list of files
        file_list = []
        for i in range(0, len(file_dir_list)):
            file_dir = file_dir_list[i]
            file_list.append(os.listdir(user_dir +"\\" +file_dir))

        # if user has a file directory yet no files        
        if file_list == [[]]:
            response='Directories are empty.'
            print(response)
            conn.send(response.encode())
        
        else:
            # if user has files, write a txt file with their names 
            with open('filenames.txt', 'w') as fh:
                for list in file_list:
                    for file in range(0, len(list)):
                        fh.write('%s\n' % list[file])
            
            # send list (the txt file) to client
            file_names=open('filenames.txt', 'rb').read()
            conn.send(file_names)
            print('\nSending file names...\n')    

            # delete the file 
            os.remove('filenames.txt')
        
        
# gets files from servers
def get(username):
    return 'Not Yet Implemented'

def control():
    while 1:
    
        # receive command from user
        command_list = ['put','list','get','exit']
        command = ''
        while command not in command_list:
            command = conn.recv(1024).decode()
        print('Command: ' +command + ' recieved.')

        # PUT
        if command == 'put':
            put(new_dir_path)

        # LIST
        elif command == 'list':
            list_files(username)

        # GET
        elif command == 'get':
            get(username)
    
        # Exit
        elif command == 'exit':
            print('User requested to exit. Server shutting down.')
            break

        # handle wrong command  
        else:
            print('Command does not exist.')
            sys.exit()

    conn.close()
    sys.exit()
    

# Start the server -------------------------------------------------  #These are out here for them to be accessible by other functions
server_name = '127.0.0.1'
server_port = int(sys.argv[1])
    
# define socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_name, server_port))
server_socket.listen(5)
print('Server listening on socket:'+str(server_port))

conn, address = server_socket.accept() #accept() return the connection object and the address of the client which is why we need 2 variables to store each.
print('Connected to Client.')
    
# get username
username = conn.recv(2048)
username = username.decode()
print('received username')
# create a new directory for user, if none exists 
new_dir_path = new_dir(username)
  
if __name__=='__main__':

    #check the arguments
    check_args()
    control()