import sys
import math
from math import exp, expm1
from algorithms import *


def drand48():
    global seed
    a = 273673163155
    c = 138
    m = 281474976710656
    n = 4294967296
    seed = (a * seed + c) % m
    x = seed >> 16
    return float(x / n)


'''
Generates random numbers using the uniform to exponential distribution.
param: 
return: list randoms, a list of random numbers that average to 1000 set lambda = lmda
'''


def exprand():
    global lmda, upperbound
    randoms = []
    for i in range(1000000):
        x = - math.log(drand48()) / lmda
        if x > upperbound:
            i -= 1
            continue
        randoms.append(x)
    return randoms


# generate the processes
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
            if j == burst - 1:
                io = 0
            else:
                io = math.ceil(sequence[count])
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
    rr_add = int(sys.argv[8]
    '''

    # hard coded test variables, remove when using command-line arguments
    seed = 2
    count = 10
    switcht = 4
    upperbound = 300
    t_cs = 4
    count = 0
    upperbound = 30
    lmda = 0.01
    alpha = 0.5
    t_slice = 20
    sequence = exprand()
    process = processGen(1)
    print_new(process)

    bne = 0
    FCFS(process, t_cs)
    RR(process, t_cs, t_slice, bne)

    # print_test(process)
    #FCFS(process, t_cs)
    #process = processGen(count)

    #SRT(process, alpha, lmda, switcht, processlist)
    # print(process)
    # print("=======test=======")
    # print(process[0]["arrival"])
    # print(FCFS(process))
    # print(len(process[0]))


    # hard coded test variables, remove when using command-line arguments
    # function calls
    '''
    # FCFS
    process = processGen(n)
    print_new(process)
    print_log(FCFS(process))
    process = processGen(n)
    print_new(process)
    print_log(SJF(process))
    process = processGen(n)
    print_new(process)
    print_log(SRT(process))
    process = processGen(n)
    print_new(process)
    print_log(RR(process, t, bne))
    '''
