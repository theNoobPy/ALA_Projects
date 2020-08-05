from numba import vectorize
import numba
import numpy as np 
import random
from timeit import default_timer as timer    

# standard serial function
def Add(a, b):
    return a + b
  
# parallelized function using nvidia GPU
@vectorize(['float32(float32, float32)'], target='cuda')
def Add_Cuda(a, b):
  return a + b
        
def main():
    N = 100000000
    A = np.ones(N, dtype=np.float32)
    B = np.ones(A.shape, dtype=A.dtype)
    C = np.empty_like(A, dtype=A.dtype)
    
    start = timer() 
    C = Add(A, B) 
    print("Result ",C ,"\nwithout GPU:", timer()-start)     
      
    start = timer() 
    C = Add_Cuda(A, B) 
    print("Result ",C ,"\nwith GPU:", timer()-start)

if __name__=="__main__": 
    main()