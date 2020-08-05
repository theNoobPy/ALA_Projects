# in this example we will create 2 threads and have them perform simple
# mathematical equations 
import threading #import thread class
import time
import datetime
import numpy
from tabulate import tabulate

def f_add(x, y, id_):
    z = x + y
    time.sleep(1)
    print("Thread Number: ",id_,"sum is:" ,z)
    
def f_sub(x, y, id_):
    z = x - y
    time.sleep(1)
    print("Thread Number: ",id_,"difference is:" ,z)
    
def f_mult(x, y, id_):
    z = x * y
    time.sleep(1)
    print("Thread Number: ",id_,"product is:" ,z)
    
def f_div(x, y, id_):
    z = x / y
    time.sleep(1)
    print("Thread Number: ",id_,"quotient is:" ,z)

#MAIN
t = [None] * 0 #math type array
x = [None] * 0
y = [None] * 0
th = [None] * 0 #thread array
table = [None] * 0 #array to contain values to put into the output table
#thread creation
t_in = "start"
while 1:

    while t_in != "Add" and t_in != "Subtract" and t_in != "Multiply" and t_in != "Divide":
        t_in = input("Add\nSubtract\nMultiply\nDivide\nEnter \"end\" to continue\n")
        if t_in == "end":
            break
        
        if t_in == "Add" or t_in == "Subtract" or t_in == "Multiply" or t_in == "Divide":
            t.append(t_in)#the type of thread
    
    if t_in == "end":
        break
    
    try:
        x.append(int(input("Enter first number ")))#the first variable
    except ValueError:
        print("Not an integer! Try again.")
        continue
    
    try:
        y.append(int(input("Enter second number ")))#the second variable
    except ValueError:
        print("Not an integer! Try again.")
        continue
    
    
    t_in = "repeat"

i = 0
for x_thread in t:
    if x_thread == "Add":
        th.append(threading.Thread(target=f_add,args=(x[i],y[i],i+1)))
    if x_thread == "Subtract":
        th.append(threading.Thread(target=f_sub,args=(x[i],y[i],i+1)))
    if x_thread == "Multiply":
        th.append(threading.Thread(target=f_mult,args=(x[i],y[i],i+1)))
    if x_thread == "Divide":
        th.append(threading.Thread(target=f_div,args=(x[i],y[i],i+1)))
    
    i = i + 1
        

#start threads
for thisthread in th:
    thisthread.start()


print("No.of threads: ",threading.active_count()) #displays no. of active threads
print("Threads Created: ", threading.enumerate()) #lists the threads
# displays  if the thread is running, which should be true

i = 1
for thisthread in th:
    table.append(['Thread',i,' status: ',str(thisthread.is_alive())])
    i = i + 1

print(tabulate(table))





end = input("press enter to end\n")