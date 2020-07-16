import sys
from queue import PriorityQueue
global processlist
processlist = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                   "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
'''
Simulates first-come-first-serve modal in CPU scheduling.
param: list data, data = [{arrival: t, 0:[cput, iot], 1:[cput, iot],...}...]
effects: none
returns: none
Note:  This implementation is analogous to RR(data, INFINITY, 0).
        Assuming data[0] is process 'A', and data[1] is process 'B', and so on.
'''


def FCFS(data):
    cpubtT = 0      # total time
    waittT = 0
    trnadT = 0
    ctsT   = 0
    prmptT = 0
    ReadyQueue = []
    arrtime = []
    dict = []
    n = len(data)
    # put process into ready queue
    for i in range(n):
        ReadyQueue.append(processlist[i])
    for i in range(n):
        arrtime.append(data[i]["arrival"])
    for i in range(n):
        for j in range(0, n - i - 1):
            if arrtime[j] > arrtime[j + 1]:
                arrtime[j], arrtime[j + 1] = arrtime[j + 1], arrtime[j]
                ReadyQueue[j], ReadyQueue[j + 1] = ReadyQueue[j + 1], ReadyQueue[j]
    burstarr = []
    for i in range(n):
        burstarr.append(len(data[i])-1)  # burstarr = [ num of burst of A, num of burst of B,...]
    for i in range(n):
        dict.append({})
        time = 1
        dict[i]["time"] = time # dict[time: time, 0:[process id], 1:[status], 2:[cpu using time],
                               #     3:[burst num], 4:[Readyqueue] ]




    return arrtime,ReadyQueue,burstarr # for test ; should be: return dict


'''
Simulats Shortest Job First CPU scheduling.
param: data, alpha, data = [{arrival: t, 0:[cput, iot], 1:[cput, iot],...}...]
        alpha for exponential averaging
effects: none
returns: none
Note: We use exponential averaging to estimate the next CPU burst time.
        Following the formula:   tau     =  alpha x t   +  (1-alpha) x tau
                                    i+1              i                    i
        , where tau is default to 10.
                                   
'''


def SJF(data, alpha):
    return 0


'''
Simulats Shortest Remaining Time CPU scheduling.
param: data, alpha, data = [{arrival: t, 0:[cput, iot], 1:[cput, iot],...}...]
        alpha for exponential averaging
effects: none
returns: none
Note: We use exponential averaging to estimate the next CPU burst time.
        Following the formula:   tau     =  alpha x t   +  (1-alpha) x tau
                                    i+1              i                    i
        , where tau is default to 10.                          
'''


def SRT(data, alpha):
    global lmda
    global switcht
    arrivq = PriorityQueue()
    readyq = PriorityQueue()
    stat = []
    tau = 1/lmda
    t = 10
    for i in range(len(data)):
        stat.append((0, data[i]["arrival"], -1))
        #arrivq.put((data[i]["arrival"], i))

    tmln = 0
    while stat.max()[0] != -1:
        for i in range(len(stat)):
            stat[i][1] = stat[i][1]-1
            if stat[i][0] == 3:
                if stat[i][1] > readyq[0][0]:
                    nextel = readyq.get()
                    stat[nextel[1]][0] = 3
                    stat[nextel[1]][1] = data[nextel[1]][stat[nextel[1]][2]][0]
                    stat[i][0] = 2
                    readyq.put((stat[i][1],i))
            if stat[i][1] == 0:#something's happening

                if stat[i][0] == 0:#arrived and queuing
                    #stat[i][2] = stat[i][2] + 1
                    #cput = data[i][stat[i][2]][0]
                    tau = t * alpha + (1 - alpha) * tau
                    stat[i][0] = 2
                    stat[i][2] = stat[i][2] + 1
                    readyq.put((tau,i))

                elif stat[i][0] == 1:#io'ed to ready queue
                    tau = t*alpha + (1-alpha)*tau
                    readyq.put((tau,i))
                    stat[i][2] = stat[i][2] + 1
                    stat[i][0] = 2
                elif stat[i][0] == 3:#finished running, to next
                    if data[i][stat[i][2]][1] == 0:#finished

                        stat[i][0] = -1
                        stat[i][1] = tmln - data[i]["arrival"]
                    else: #to next
                        stat[i][0] = 1
                        stat[i][2] = stat[i][2]
                        nextel = readyq.get()
                        stat[nextel[1]][0] = 4
                        stat[nextel[1]][1] = switcht
                        # stat[nextel[1]][1] = data[nextel[1]][stat[nextel[1]][2]][0]
                else:#switched, start cpu
                    stat[i][0] = 3
                    stat[i][1] = data[i][stat[i][2]][0]

        tmln = tmln+1

    return 0


'''
Simulates Round-Robin modal in CPU scheduling. 
param: list data, t, bne, data = [{arrival: t, 0:[cput, iot], 1:[cput, iot],...}...],
 t = time slice, bne = beginning or end of the sequence
effects: none
returns: none
Note: Assuming data[0] is process 'A', and data[1] is process 'B', and so on.
        If 0 is given for bne, the default is END.
'''


def RR(data, time, bne):
    if bne == 0:
        bne = True
    else:
        if bne == "BEGINNING":
            bne = False
        else:
            bne = True

    return 0

