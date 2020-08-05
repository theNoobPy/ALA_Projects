
import multiprocessing
from multiprocessing import Pool
import time
import os
def getSquareK(x):
  sum=0
  for x in range(10000):
    sum+=x*x
  return sum
 
def ChildMaking(): 
  # printing process id 
  print("Child Process ID: {}".format(os.getpid())) 



if __name__=="__main__": 
  print("\n**Multiprocessing with map and reduce demo**")
  print("Main Process ID: {}".format(os.getpid())) 
  print("1. Compare execution time of mapReduced parallel vs serial computing the squares of 1-10000")
  print("2. Create a child process and verify its process id ")
  ch = int(input(" Select : "))
  if ch == 1:
    print("We will map a processing pool with the task of squaring numbers 1 to 10000 and\na single process with the same task")
    time.sleep(4)
    print("Executing... \n")
    poolTime=time.time()
    pool=Pool() #declare pool object
    result=pool.map(getSquareK,range(10000))# divide the tasks to individual cores
    pool.close()# these two lines of code will return the result only when the tasks have been completed
    pool.join()#

    print("Pool took: " ,time.time()-poolTime) # displays the amount of time parallel computing took

    #assigning a task without using parallel computing
    SerialTime=time.time()
    result= []
    for x in range(10000):
      result.append(getSquareK(x))

    print ("Serial processing took: ",time.time()-SerialTime)
    print ("As you can see parallel computing is much efficient\nthan serial as it utilizes all cpu cores")
    time.sleep(100)
  if ch == 2:
    p1 =multiprocessing.Process(target=ChildMaking) 
    p1.start()
  
    p1.join()



  else:
    print("Invalid input")

  