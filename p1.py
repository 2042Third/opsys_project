import sys
import math
from queue import PriorityQueue
from math import exp, expm1
from algorithms import *

def srand48(seed):
    global x
    x = seed << 16 + 0x330e

def drand48():
    global x
    a = 25214903917
    c = 11
    m = 281474976710656
    n = 4294967296
    x = (a * x + c) & (m-1)
    y = x / m
    return y


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


    n = int(sys.argv[1])
    seed = int(sys.argv[2])
    lmda = float(sys.argv[3])
    upperbound = int(sys.argv[4])
    t_cs  = int(sys.argv[5])
    alpha = float(sys.argv[6])
    t_slice = float(sys.argv[7])
    bne = int(sys.argv[8])


    # hard coded test variables, remove when using command-line arguments
    switcht = 0
    switcht = t_cs


    count = 0



    x = 0
    srand48(seed)
    sequence = exprand()
    process = processGen(2)
    print_new(process)
    # print_test(process)
    bne = 0

    # print_test(process)
    #FCFS(process, t_cs)
    # print_test(process)
    ##FCFS(process, t_cs)
    #process = processGen(count)

    # print(process)
    # print("=======test=======")
    # print(process[0]["arrival"])
    # print(FCFS(process))
    # print(len(process[0]))


    # hard coded test variables, remove when using command-line arguments
    # function calls
    '''
    # FCFS
    
    '''

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
