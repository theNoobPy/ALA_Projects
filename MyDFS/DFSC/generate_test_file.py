#import re
import os
import sys
#import glob
import time
#import pickle
import socket
#import hashlib

textList = "0"

for i in range(1, 1000001):
  textList += "\n"+str(i)

outF = open("Test_File.txt", "w")
for line in textList:
  # write line to output file
  outF.write(line)
outF.close()





















