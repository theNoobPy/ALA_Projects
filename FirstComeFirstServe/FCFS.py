
def getWaitTime(processes, n, 
                    burstTime, waitTime): 
    #initialize wait time as 0
    waitTime[0] = 0 
    for i in range(1, n ): 
        waitTime[i] = burstTime[i - 1] + waitTime[i - 1]  
  
#calculates turaround time
def getTurnAroundTime(processes, n,  
                       burstTime, waitTime, turnAroundTime):  
    for i in range(n): 
        turnAroundTime[i] = burstTime[i] + waitTime[i] 
#calculates the average time of the [rpcesses] 
def getAveTime( processes, n, burstTime): 
  
    waitTime = [0] * n 
    turnAroundTime = [0] * n  
    total_waitTime = 0
    total_turnAroundTime = 0
  
#displays waiting time of the processes
    getWaitTime(processes, n, burstTime, waitTime) 
  
#displayes turnaround time of processes
    getTurnAroundTime(processes, n,  
                       burstTime, waitTime, turnAroundTime) 
  
#displays a table containing the details of the processes
    print( "Processes Burst time " + 
                  " Waiting time " + 
                " Turn around time") 
  
#calculates total wait and turnaround time
    for i in range(n): 
      
        total_waitTime = total_waitTime + waitTime[i] 
        total_turnAroundTime = total_turnAroundTime + turnAroundTime[i] 
        print(" " + str(i + 1) + "\t\t" + 
                    str(burstTime[i]) + "\t " + 
                    str(waitTime[i]) + "\t\t " + 
                    str(turnAroundTime[i]))  
  
    print( "Average waiting time = "+
                   str(total_waitTime / n)) 
    print("Average turn around time = "+
                     str(total_turnAroundTime / n)) 
  
#main 
if __name__ =="__main__": 
    print("First Come First Serve Demo")
    # get number of processes
    n=int(input("Enter number of processes: "))
    processes = [0] * n
    burst_time = []
    
    #asks for the burst time of each process
    for i in range(0, n):
        item = int(input("Enter burst time of process ", i + 1, ":"))
        burst_time.append(item)
    getAveTime(processes, n, burst_time) 
            






        