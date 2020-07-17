import sys
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


def FCFS(data, tcs):
    processlist = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                   "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    print("time 0ms: Simulator started for FCFS [Q <empty>]")
    waittT = 0
    trnadT = 0
    ctsT   = 0
    prmpt = 0
    queue = []
    nextaction = []
    burstleft = []
    burstdone = []
    using = 0
    first_process = 1
    for i in range(len(data)):
        nextaction.append(("arrive", data[i]["arrival"]))
        burstleft.append(len(data[i]) - 2)
        burstdone.append(0)
    finish = 0
    time = 0
    while finish < len(data):
        actions = []
        for i in range(len(data)):
            if time == nextaction[i][1]:
                actions.append((i, nextaction[i]))
        if len(actions) > 1:
            prmpt += 1
        for i in range(len(actions)):
            if actions[i][1][0] == "arrive":
                queue.append(processlist[actions[i][0]])
                if time <= 999:
                    print("time {}ms: Process {} arrived; added to ready queue [Q {}"
                          .format(time, processlist[actions[i][0]], queue[0]), end="")
                    for j in range(1, len(queue)):
                        print("", queue[j], end="")
                    print("]")
            elif actions[i][1][0] == "cpu":
                current = actions[i][0]
                queue.pop(0)
                nextaction[current] = ("io", time + data[current][burstdone[current]][0])
                if time <= 999:
                    print("time {}ms: Process {} started using the CPU for {}ms burst [Q "
                          .format(time, processlist[current], data[current][burstdone[current]][0]), end="")
                    if len(queue) == 0:
                        print("<empty>]")
                    else:
                        print(queue[0], end="")
                        for j in range(1, len(queue)):
                            print("", queue[j], end="")
                        print("]")
            elif actions[i][1][0] == "io":
                current = actions[i][0]
                burstleft[current] -= 1
                burstdone[current] += 1
                if burstleft[current] == 0:
                    print("time {}ms: Process {} terminated [Q ".format(time, processlist[current]), end="")
                    if len(queue) == 0:
                        print("<empty>]")
                    else:
                        print(queue[0], end="")
                        for j in range(1, len(queue)):
                            print("", queue[j], end="")
                        print("]")
                    finish += 1
                else:
                    nextaction[current] = ("ready", time + data[current][burstdone[current]][1])
                    if time <= 999:
                        print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q "
                              .format(time, processlist[current], burstleft[actions[i][0]]), end="")
                        if len(queue) == 0:
                            print("<empty>]")
                        else:
                            print(queue[0], end="")
                            for j in range(1, len(queue)):
                                print("", queue[j], end="")
                            print("]")
                        print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q "
                              .format(time, processlist[current], nextaction[current][1]), end="")
                        if len(queue) == 0:
                            print("<empty>]")
                        else:
                            print(queue[0], end="")
                            for j in range(1, len(queue)):
                                print("", queue[j], end="")
                            print("]")
                using = 0
            elif actions[i][1][0] == "ready":
                queue.append(processlist[actions[i][0]])
                if time <= 999:
                    print("time {}ms: Process {} completed I/O; added to ready queue [Q {}"
                          .format(time, processlist[actions[i][0]], queue[0]), end="")
                    for j in range(1, len(queue)):
                        print("", queue[j], end="")
                    print("]")
        if len(queue) > 0 and using == 0:
            current = processlist.index(queue[0])
            using = 1
            if first_process == 1:
                nextaction[current] = ("cpu", time + tcs/2)
                first_process = 0
            else:
                nextaction[current] = ("cpu", time + tcs)
        time += 1
    print("time {}ms: Simulator ended for FCFS [Q <empty>]".format(time+1))
    return 0


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

