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
    neighbor = 0 #this is the port number of the neighbor
    ht_id = 0
    Table = ['empty'] * HT_SIZE_LIMIT
    
    def __init__(self, neighbor, ht_id):
        self.neighbor = ('127.0.0.1', int(neighbor))
        self.ht_id = ht_id
        
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
    
    
    
print(allocate_keys(10))

ht = Hash_Table(int(1),1)

k = 0
while k != 100:
    insert_me = Key_N_Data(k,'Kevin'+str(k),'abc')
    ht.ins_tab(insert_me)
    k+=1

ht.query(72,'Kevin72').Data = 'Joker'


try:
    print(str(ht.query(72,'Kevin12').Data))
except:
    print('not found')
    
print(ht.delete(1,'Kevin69'))

insert_me = Key_N_Data(1,'Kevin72','abc')
print(ht.ins_tab(insert_me))

try:
    print(str(ht.query(72,'Kevin69').Data))
except:
    print('not found')


