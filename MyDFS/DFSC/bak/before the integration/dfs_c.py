#import re
import os
import sys
#import glob
import time
#import pickle
import socket
#import hashlib

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

	global command
	command = ''
	while 1:
		if command == 'get' or command == 'list' or command == 'put':
			return command
			break
		else:
			comm = input('Input Command [get, list, put]: ')
			if comm.lower() == 'get':
				command = 'get'
				continue
			elif comm.lower() == 'list':
				command = 'list'
				continue
			elif comm.lower() == 'put':
				command = 'put'
				continue
			else:
				print('Invalid Command.')
				continue



	
# define client socket connection
def client():
	# config params for servers
	server_list = server_conf()
	connected = 0
	conns = list()
	
	for i in range(len(server_list)):
		#Connect to servers specified
		try:
			conns.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
			conns[i].connect(server_list[i])
			status_s = ('Connected to server#', str(i+1))
			print(status_s[0], status_s[1])
			connected = 1
			time.sleep(1)
		except ConnectionRefusedError:
			print('Could not connect to server#', i+1)
	
	
		
	#All servers down
	if connected == 0:
		print('No servers are online. System shutting down.')
		sys.exit()
		
    
    #send username
	username = input('Enter username: ')
    
    
	try:
		for i in range(len(conns)):
			conns[i].send(username.encode())
	except OSError:
		pass
    
	# get command from user -------------------------------
	get_command()



# run client
if __name__=='__main__':
	client()