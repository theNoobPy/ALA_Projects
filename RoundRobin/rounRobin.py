"""Round Robin is a pre-emptive algorithm that is mainly used by network schedulers in computing
Time-slices are  assigned to each process  in equal proportions and in a circular manner
it handles  all processes without priority
RoundRobin scheduling in Python Demo
"""
def getWaitingTime(processes, n, burstTime,  
                         WaitingTime, quantum):  
    remainingBurstT = [0] * n 
  
    # initialize the remaining burst time to new burst time of process
    for i in range(n):  
        remainingBurstT[i] = burstTime[i] 
    t = 0 # Current time  
  
    #round robin implementation
    while(1): 
        done = True
  
        #code for scanning and checking proccesses
        for i in range(n): 
              
            # If burst time > 0 ,proceed 
            if (remainingBurstT[i] > 0) : 
                done = False # boolean is false when a process is still active
                  
                if (remainingBurstT[i] > quantum) : 
                  
                     
                    t += quantum  
  
                   # after incrementing time, this code decreases the burst time by the value of quantum
                    remainingBurstT[i] -= quantum  
                  
               
                # when the burst time of the current process is <=0 then this will be its last cycle
                else: 
                    t = t + remainingBurstT[i]  
  
                    WaitingTime[i] = t - burstTime[i]  
  
                    remainingBurstT[i] = 0 #process has been completed
                  
        # sets the boolean to true when all the processes are dun
        if (done == True): 
            break
              
#  Calculate turn around time  
def getTurnAroundTime(processes, n, burstTime, WaitingTime, tat): 
      
    # Calculating turnaround time  
    for i in range(n): 
        tat[i] = burstTime[i] + WaitingTime[i]  
  
  
# Function to calculate average waiting and turn-around times.
def getAvgTime(processes, n, burstTime, quantum):  
    WaitingTime = [0] * n 
    tat = [0] * n  

    getWaitingTime(processes, n, burstTime,  
                         WaitingTime, quantum)  
  
   
    getTurnAroundTime(processes, n, burstTime, 
                                WaitingTime, tat)  
  
    # Displays a detailed table about the processes
    print("Processes    Burst Time     Waiting",  
                     "Time    Turn-Around Time") 
    total_WaitingTime = 0
    totalTurnArTime = 0
    for i in range(n): 
  
        total_WaitingTime = total_WaitingTime + WaitingTime[i]  
        totalTurnArTime = totalTurnArTime + tat[i]  
        print(" ", i + 1, "\t\t", burstTime[i],  
              "\t\t", WaitingTime[i], "\t\t", tat[i]) 
  
    print("\nAverage waiting time = %.5f "%(total_WaitingTime /n) ) 
    print("Average turn around time = %.5f "% (totalTurnArTime / n))  
      

if __name__ =="__main__": 
      
   # get number of processes
    n=int(input("Enter number of processes: "))
    proc = [0] * n
    burst_time = []

    #asks for the burst time of each process
    for i in range(0, n):
        print("Enter burst time of process", i, ":")
        item = int(input())
        burst_time.append(item)
  
      
    quantum = 2
    getAvgTime(proc, n, burst_time, quantum) 
  
