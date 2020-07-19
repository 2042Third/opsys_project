import sys
import math
from queue import PriorityQueue
from math import exp, expm1
from algorithms import *

# def srand48(seed):
#     global x
#     x = seed << 16 + 0x330e
#
# def drand48():
#     global x
#     a = 25214903917
#     c = 11
#     m = 281474976710656
#     n = 4294967296
#     x = (a * x + c) & (m-1)
#     y = x / m
#     return y

class Rand48(object):
    def __init__(self, seed):
        self.n = seed
    def seed(self, seed):
        self.n = seed
    def srand(self, seed):
        self.n = (seed << 16) + 0x330e
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    def drand(self):
        return self.next() / 2**48
    def lrand(self):
        return self.next() >> 17
    def mrand(self):
        n = self.next() >> 16
        if n & (1 << 31):
            n -= 1 << 32
        return n

'''
Generates random numbers using the uniform to exponential distribution.
param: 
return: list randoms, a list of random numbers that average to 1000 set lambda = lmda
'''


def exprand(seed):
    global lmda, upperbound
    rand = Rand48(seed)
    rand.srand(seed)
    randoms = []
    for i in range(1000000):
        x = ((-1)* math.log(rand.drand())) / lmda
        if x > upperbound:
            i -= 1
            # print(x)
            continue
        randoms.append(x)
    return randoms


# generate the processes (on page5)
# n: the number of process generates (1<=n<=26)
# using the drand() to identify the number of bursts time; using the exp-random to identify the cpu and I/O burst time
def processGen(n):
    # list of process dictionaries
    global sequence, rand, lmda

    count = 0
    rand.srand(seed)
    process = []
    for i in range(n):
        x = ((-1) * math.log(rand.drand())) / lmda
        if x > upperbound:
            x = ((-1) * math.log(rand.drand())) / lmda


        arrival = math.floor(x)
        count += 1
        # print(sequence[0],sequence[1],sequence[2])
        process.append({})
        #count += 4
        process[i]["arrival"] = arrival

        burst = int(100 * rand.drand()) + 1
        count += 1
        # print(sequence[3], sequence[4], sequence[5])
        # if(burst > 100):
        #     continue
        for j in range(burst):
            x = ((-1) * math.log(rand.drand())) / lmda
            if x > upperbound:
                x = ((-1) * math.log(rand.drand())) / lmda
            cpu = math.ceil(x)
            count += 1
            if j == burst - 1:
                io = 0
            else:
                x = ((-1) * math.log(rand.drand())) / lmda
                if x > upperbound:
                    x = ((-1) * math.log(rand.drand())) / lmda
                io = math.ceil(x)
                count += 1
            process[i][j] = (cpu, io)
    return process


'''
Print out the initial process arrival time and CPU bursts
param: 
process: the process list of dictionaries
'''


def print_new(process):
    processlist = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                   "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    for i in range(len(process)):
        print("Process", processlist[i], "[NEW] (arrival time", process[i]["arrival"],
              "ms)", len(process[i].keys()) - 1, "CPU bursts")


'''
For test only
Print out the detail CPU bursts and I/O bursts
param: 
process: the process list of dictionaries
'''


def print_test(process):
    processlist = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                   "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    for i in range(len(process)):
        print("Process", processlist[i], "\nArrival time:", process[i]["arrival"], "ms")
        print("CPU BURSTS:")
        for j in range(len(process[i].keys()) - 1):
            print("CPU burst time:", process[i][j][0], "ms  I/O burst time:", process[i][j][1], "ms")


# handle the ties in the order: CPU burst completion, I/O, new proces
'''
requires: a and b are not null
params: char a , char b; process id's 
effects: none
returns: char t, the smaller name character
'''


def handleTies(a, b):
    if (a < b):
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
    lmda = float(sys.argv[3])
    upperbound = int(sys.argv[4])
    t_cs  = int(sys.argv[5])
    alpha = float(sys.argv[6])
    t_slice = float(sys.argv[7])
    '''
    n = 2
    seed = 2
    lmda = 0.01
    upperbound = 256
    t_cs = 4
    alpha = 0.5
    t_slice = 128
    bne = 'END'
    rand = Rand48(seed)
    switcht = 0
    switcht = t_cs
    count = 0
    x = 0
    # rand.srand(seed)
    sequence = exprand(seed)

    process = processGen(n)

    bne = 0

    f = open("simout.txt", "w")
    f.write("Algorithm FCFS\n")
    print_new(process)
    result = FCFS(process, t_cs)
    f.write("-- average CPU burst time: {:.3f} ms\n".format(result[0]))
    f.write("-- average wait time: {:.3f} ms\n".format(result[1]))
    f.write("-- average turnaround time: {:.3f} ms\n".format(result[2]))
    f.write("-- total number of context switches: {}\n".format(result[3]))
    f.write("-- total number of preemptions: {}\n".format(result[4]))

    f.write("Algorithm SJF\n")
    result = SJF(process, alpha, lmda, switcht, processlist)
    f.write("-- average CPU burst time: {:.3f} ms\n".format(result[0]))
    f.write("-- average wait time: {:.3f} ms\n".format(result[1]))
    f.write("-- average turnaround time: {:.3f} ms\n".format(result[2]))
    f.write("-- total number of context switches: {}\n".format(result[3]))
    f.write("-- total number of preemptions: {}\n".format(result[4]))
    f.write("Algorithm SRT\n")
    result = SRT(process, alpha, lmda, switcht, processlist)
    f.write("-- average CPU burst time: {:.3f} ms\n".format(result[0]))
    f.write("-- average wait time: {:.3f} ms\n".format(result[1]))
    f.write("-- average turnaround time: {:.3f} ms\n".format(result[2]))
    f.write("-- total number of context switches: {}\n".format(result[3]))
    f.write("-- total number of preemptions: {}\n".format(result[4]))
    print_new(process)
    f.write("Algorithm RR\n")
    result = RR(process, t_cs, t_slice, bne)
    f.write("-- average CPU burst time: {:.3f} ms\n".format(result[0]))
    f.write("-- average wait time: {:.3f} ms\n".format(result[1]))
    f.write("-- average turnaround time: {:.3f} ms\n".format(result[2]))
    f.write("-- total number of context switches: {}\n".format(result[3]))
    f.write("-- total number of preemptions: {}\n".format(result[4]))

    #print(sequence)
