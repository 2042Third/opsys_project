import sys
import math
from algorithms import *
def drand48():
  global seed
  a = 273673163155
  c = 138
  m = 281474976710656
  n = 4294967296
  seed = (a * seed + c) % m
  x = seed >> 16
  return float (x / n)



# generate the processes (on page5)
# n: the number of process generates (1<=n<=26)
# using the drand() to identify the number of bursts time; using the exp-random to identify the cpu and I/O burst time
def processGen(n):
  # list of process dictionaries
  global sequence
  count = 0
  process = []
  for i in range(n):
    arrival = math.floor(sequence[count])
    count += 1
    process.append({})
    process[i]["arrival"] = arrival
    burst = int(100 * drand48()) + 1
    for j in range(burst):
      cpu = math.ceil(sequence[count])
      count += 1
      if j == burst-1:
        io = 0
      else:
        io = math.ceil(sequence[count])
        count += 1
      process[i][j] = (cpu, io)
  return process

def print_new(process):
  processlist = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                 "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
  for i in range(len(process)):
    print("Process", processlist[i], "[NEW] (arrival time", process[i]["arrival"],
          "ms)", len(process[i].keys())-1, "CPU bursts")

#handle the ties in the order: CPU burst completion, I/O, new proces
'''
requires: a and b are not null
params: char a , char b; process id's 
effects: none
returns: char t, the smaller name character
'''
def handleTies(a , b):
  if(a < b):
    return a
  else:
    return b

if __name__ == '__main__':
  # list of processes
  processlist = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                 "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
  # get all the cmd/parameters

  '''
  n = int(sys.argv[1])
  seed = int(sys.argv[2])
  Lambda = float(sys.argv[3])
  upperbound = int(sys.argv[4])
  t_cs  = int(sys.argv[5])
  alpha = float(sys.argv[6])
  t_slice = float(sys.argv[7])
  rr_add = int(sys.argv[8]
  '''

  seed = 100
  sequence = []
  min = 0
  max = 0
  sum = 0
  for i in range(1000):
    x = -math.log(drand48()) / 0.001
    if x > 3000:
      i -= 1
    sequence.append(x)
  # print(sequence)
  process = processGen(10)
  print_new(process)