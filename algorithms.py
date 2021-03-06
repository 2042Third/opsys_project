import sys
import math
from queue import PriorityQueue
from p1 import handleTies

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
    print("time 0ms: Simulator started for FCFS [Q <empty>]")
    cts = 0
    prmpt = 0
    queue = []
    nextaction = []
    burstleft = []
    burstdone = []
    using = 0
    first_process = 1
    avgburst = 0
    runtime = []
    burstcount = 0
    content_switch = 0
    sumburst = 0
    wait = []
    for i in range(len(data)):
        nextaction.append(("arrive", data[i]["arrival"]))
        runtime.append(data[i]["arrival"])
        burstleft.append(len(data[i]) - 1)
        burstdone.append(0)
        wait.append([])
        for j in range(len(data[i]) - 1):
            wait[i].append(0)
            sumburst += data[i][j][0]
            burstcount += 1
    avgburst = sumburst / burstcount
    finish = 0
    time = 0
    while finish < len(data):
        actions = []
        for i in range(len(data)):
            if time == nextaction[i][1]:
                actions.append((i, nextaction[i]))
        for j in range(len(actions)):
            for i in range(len(actions) - 1):
                if actions[i][1][0] != "cpu" and actions[i+1][1][0] == "cpu":
                    temp = actions.pop(i)
                    actions.append(temp)
        for i in range(len(actions)):
            current = actions[i][0]
            if actions[i][1][0] == "arrive":
                queue.append(processlist[actions[i][0]])
                wait[current][burstdone[current]] = time
                if time <= 999:
                    print("time {}ms: Process {} arrived; added to ready queue [Q {}"
                          .format(time, processlist[actions[i][0]], queue[0]), end="")
                    for j in range(1, len(queue)):
                        print("", queue[j], end="")
                    print("]")
            elif actions[i][1][0] == "cpu":
                wait[current][burstdone[current]] = time - wait[current][burstdone[current]] - tcs/2
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
                burstleft[current] -= 1
                burstdone[current] += 1
                content_switch = time + tcs/2
                if burstleft[current] == 0:
                    runtime[current] = time - runtime[current]
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
                    nextaction[current] = ("ready", int(time + data[current][burstdone[current]-1][1] + tcs/2))
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
                wait[current][burstdone[current]] = time
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
                cts += 1
            elif time <= content_switch:
                nextaction[current] = ("cpu", content_switch + tcs/2)
                cts += 1
            else:
                nextaction[current] = ("cpu", time + tcs/2)
                cts += 1
        time += 1
    print("time {}ms: Simulator ended for FCFS [Q <empty>]".format(time+1))
    sumwait = 0
    for i in range(len(data)):
        for j in range(len(wait[i])):
            sumwait += wait[i][j]
    avgwait = sumwait / burstcount
    avgtrn = avgburst + avgwait + tcs
    result = [avgburst, avgwait, avgtrn, cts, prmpt]
    return result


'''
Simulates Round-Robin modal in CPU scheduling. 
param: list data, t, bne, data = [{arrival: t, 0:[cput, iot], 1:[cput, iot],...}...],
 t = time slice, bne = beginning or end of the sequence
effects: none
returns: none
Note: Assuming data[0] is process 'A', and data[1] is process 'B', and so on.
        If 0 is given for bne, the default is END.
'''


def RR(data, tcs, t_slice, bne):
    if bne == "BEGINNING":
        bne = False
    else:
        bne = True
    print("time 0ms: Simulator started for RR [Q <empty>]")
    cts = 0
    prmpt = 0
    queue = []
    nextaction = []
    burstleft = []
    burstdone = []
    wait = []
    timeleft = []
    using = 0
    first_process = 1
    runtime = []
    burstcount = 0
    content_switch = 0
    bursts = 0
    sumburst = 0
    for i in range(len(data)):
        nextaction.append(("arrive", data[i]["arrival"]))
        burstleft.append(len(data[i]) - 1)
        burstdone.append(0)
        timeleft.append(0)
        wait.append([])
        runtime.append(data[i]["arrival"])
        for j in range(len(data[i]) - 1):
            bursts += 1
            sumburst += data[i][j][0]
    avgburst = sumburst / bursts
    finish = 0
    time = 0
    while finish < len(data):
        actions = []
        for i in range(len(data)):
            if time == nextaction[i][1]:
                actions.append((i, nextaction[i]))
        for i in range(len(actions)):
            current = actions[i][0]
            if actions[i][1][0] == "arrive":
                queue.append(processlist[current])
                wait[current].append(time)
                if time <= 999:
                    print("time {}ms: Process {} arrived; added to ready queue [Q {}"
                          .format(time, processlist[actions[i][0]], queue[0]), end="")
                    for j in range(1, len(queue)):
                        print("", queue[j], end="")
                    print("]")
            elif actions[i][1][0] == "cpu":
                burstcount += 1
                wait[current][-1] = time - wait[current][-1] - tcs/2
                if data[current][burstdone[current]][0] > t_slice:
                    nextaction[current] = ("expire", time + t_slice)
                    timeleft[current] = int(data[current][burstdone[current]][0] - t_slice)
                else:
                    nextaction[current] = ("io", time + data[current][burstdone[current]][0])
                    timeleft[current] = 0
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
                burstleft[current] -= 1
                burstdone[current] += 1
                content_switch = time + tcs/2
                if burstleft[current] == 0:
                    runtime[current] = time - runtime[current]
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
                    nextaction[current] = ("ready", int(time + data[current][burstdone[current]-1][1] + tcs/2))
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
                wait[current].append(time)
                if time <= 999:
                    print("time {}ms: Process {} completed I/O; added to ready queue [Q {}"
                          .format(time, processlist[actions[i][0]], queue[0]), end="")
                    for j in range(1, len(queue)):
                        print("", queue[j], end="")
                    print("]")
            elif actions[i][1][0] == "expire":
                content_switch = time + tcs / 2
                if timeleft[current] == 0:
                    tleft = int(data[current][burstdone[current]][0] - t_slice)
                    timeleft[actions[i][0]] = tleft
                else:
                    tleft = int(timeleft[current])
                if len(queue) == 0:
                    if time <= 999:
                        print("time {}ms: Time slice expired; no preemption because ready queue is empty [Q <empty>]"
                              .format(time))
                    nextaction[current] = ("io", time + tleft)
                else:
                    wait[current].append(time + tcs / 2)
                    nextaction[current] = ("add", int(time + tcs/2))
                    if time <= 999:
                        print("time {}ms: Time slice expired; process {} preempted with {}ms to go [Q "
                              .format(time, processlist[actions[i][0]], tleft), end="")
                        if len(queue) == 0:
                            print("<empty>]")
                        else:
                            print(queue[0], end="")
                            for j in range(1, len(queue)):
                                print("", queue[j], end="")
                            print("]")
                    prmpt += 1
                    using = 0
            elif actions[i][1][0] == "continue":
                burstcount += 1
                wait[current][-1] = time - wait[current][-1] - tcs/2
                if time <= 999:
                    print("time {}ms: Process {} started using the CPU with {}ms burst remaining [Q "
                          .format(time, processlist[current], timeleft[current]), end="")
                    if len(queue) == 0:
                        print("<empty>]")
                    else:
                        print(queue[0], end="")
                        for j in range(1, len(queue)):
                            print("", queue[j], end="")
                        print("]")
                if timeleft[current] > t_slice and finish != len(data) - 1:
                    nextaction[current] = ("expire", time + t_slice)
                    timeleft[current] -= t_slice
                else:
                    nextaction[current] = ("io", time + timeleft[current])
                    timeleft[current] = 0
            elif actions[i][1][0] == "add":
                if bne:
                    queue.append(processlist[current])
                else:
                    queue.insert(0, processlist[current])
                nextaction[current] = ("continue", 0)
        if len(queue) > 0 and using == 0:
            current = processlist.index(queue[0])
            queue.pop(0)
            using = 1
            cts += 1
            if nextaction[current][0] == "continue":
                if time <= content_switch:
                    nextaction[current] = ("continue", content_switch + tcs / 2)
                else:
                    nextaction[current] = ("continue", time + tcs / 2)
            else:
                if first_process == 1:
                    nextaction[current] = ("cpu", time + tcs / 2)
                    first_process = 0
                elif time <= content_switch:
                    nextaction[current] = ("cpu", content_switch + tcs / 2)
                else:
                    nextaction[current] = ("cpu", time + tcs / 2)
        time += 1
    print("time {}ms: Simulator ended for RR [Q <empty>]".format(time + 1))
    sumwait = 0
    for i in range(len(wait)):
        for j in range(len(wait[i])):
            sumwait += wait[i][j]
    avgwait = sumwait / bursts
    avgtrn = avgburst + avgwait + tcs + (tcs * prmpt / bursts)
    result = [avgburst, avgwait, avgtrn, cts, prmpt]
    return result


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

def print_q(i,tmln, readyq):
    print("[Q",end='')
    if len(readyq.queue) == 0:
        print("<empty>]")
    else:
        for z in range(len(readyq.queue)):
            print(" {}".format(processlist[readyq.queue[z][1]]), end="")
        print(']')

def SJF(data, alpha,lmda,switcht, processlist):
    ttcpu = 1
    ccpu = 1
    waitt = 1
    waitc = 1
    swchc = 1
    preec = 1
    remain = []
    arrivq = PriorityQueue()
    readyq = PriorityQueue()
    stat = []
    tau = 1 / lmda
    t = 10
    swchto = 'n'
    swchnum = -1
    running = -1
    finished = 0
    bursc = 0
    for i in range(len(data)):
        stat.append((0, data[i]["arrival"], -1, tau))
        remain.append(-1)
        print('Process', processlist[i], "[NEW] (arrival time", stat[i][1], "ms)", len(data[i]) - 1, 'CPU bursts')
        bursc = bursc + len(data[i]) - 1
        # arrivq.put((data[i]["arrival"], i))
        # print(stat[i])

    tmln = 0
    print('time 0ms: Simulator started for SJF [Q <empty>]')
    while max(stat)[0] != -1:

        # print(tmln,"new")
        # print(switcht)
        for i in range(len(data)):

            # print(stat, i)
            if stat[i][0] == -1:
                continue

            # print(stat[i][0],running,stat[i][0])
            if stat[i][0] == 2 and running == -2 :
                if len(readyq.queue) != 0:
                    # print('very not ')
                    swchnum = i
                    tp = stat[readyq.get()[1]]
                    waitt = waitt + tp[1] * -1
                    stat[i] = (4, switcht/2 - 1, tp[2], tp[3])

            if stat[i][1] == 0:  # something's happening
                # print("not rifhgt")
                if stat[i][0] == 0:  # arrived and queuing

                    tp = stat[i]
                    waitt = waitt + tp[1] * -1
                    stat[i] = (2, tp[1], tp[2] + 1, tp[3])
                    readyq.put((tau, i))
                    if tmln < 1000:
                        print('time {}ms: Process {} (tau {}ms) arrived; added to ready queue '
                              .format(tmln, processlist[i], stat[i][3]), end='')
                        print_q(i, tmln, readyq)
                    if swchnum == -1:  # first CPU use
                        tp = stat[i]
                        waitt = waitt + tp[1] * -1
                        readyq.get()
                        swchnum = i
                        # print(switcht)
                        stat[i] = (4, switcht/2, tp[2], tp[3])


                elif stat[i][0] == 1:  # io'ed to ready queue
                    tp = stat[i]
                    waitc = waitc + 1
                    waitt = waitt + tp[1] * -1
                    stat[i] = (2, -1, tp[2] + 1, tp[3])
                    readyq.put((stat[i][3], i))
                    if tmln < 1000:
                        print("time {}ms: Process {} (tau {}ms) completed I/O;".format(tmln,processlist[i],stat[i][3]),end='')
                        print('added to ready queue ',end='')
                        print_q(i, tmln, readyq)

                elif stat[i][0] == 3:  # finished running, to next
                    running = -2
                    # stat[i][4] = t * alpha + (1 - alpha) * stat[i][4]
                    # print(stat[i][3] * alpha + (1 - alpha) * data[i][stat[i][2]][0])
                    tptau = stat[i][3] * alpha + (1 - alpha) * data[i][stat[i][2]][0]
                    tptau = math.ceil(tptau)
                    if tmln < 1000:
                        print(
                            'time {}ms: Process {} (tau {}ms) completed a CPU burst;'.format(tmln, processlist[i],
                                                                                             stat[i][3]),
                            end='')
                        print(' {} bursts to go '.format(len(data[i])-stat[i][2]-2), end='')
                        print_q(i, tmln, readyq)
                        print(
                            'time {}ms: Recalculated tau = {}ms for process {} '.format(tmln, tptau, processlist[i], ),
                            end='')
                        print_q(i, tmln, readyq)
                    if len(readyq.queue) == 0 and data[i][stat[i][2]][1] != 0 and len(stat) != 1:
                        # print('1123123123',finished)
                        if tmln < 1000:


                            print(
                                'time {}ms: Process {} switching out of CPU;'.format(tmln, processlist[i]),
                                end='')
                            print(' will block on I/O until time {}ms '.format(data[i][stat[i][2]][1] + tmln+switcht), end='')
                            print_q(i, tmln, readyq)
                        # if finished == len(stat) - 1:
                        tp = stat[i]
                        swchto = 'io'
                        running = -2
                        waitt = waitt + tp[1]*-1
                        stat[i] = (4, switcht, tp[2]+1, tptau)
                        if data[i][stat[i][2]][1] == 0:
                            # print('1')
                            tp = stat[i]
                            stat[i] = (-1, tmln - data[i]["arrival"], tp[2], tptau)
                            finished = finished + 1
                        # continue
                    # else:
                    #     continue

                    elif data[i][stat[i][2]][1] == 0:  # finished
                        # print('2',finished)
                        if (finished == len(stat)):
                            print("time {}ms: Simulator ended for SJF [Q <empty>]".format(tmln))
                            return
                        tp = stat[i]
                        stat[i] = (-1, tmln - data[i]["arrival"], tp[2], tptau)
                        finished = finished + 1

                        if len(readyq.queue) == 0:
                            tp = stat[i]
                            running = -2
                            stat[i] = (tp[0], tp[1] - 1, tp[2], tptau)
                            continue
                        nextel = readyq.get()
                        tp = stat[nextel[1]]
                        waitt = waitt + tp[1] * -1
                        stat[nextel[1]] = (4, switcht, tp[2], tptau)
                        swchnum = nextel[1]

                    else:  # to next
                        # print('3')
                        tp = stat[i]
                        waitt = waitt + tp[1] * -1
                        stat[i] = (4, switcht/2, tp[2], tptau)

                        timediv = 2
                        swchto = 'io'
                        swchnum = -1
                        if len(readyq.queue) >= 1:
                            timediv = 1
                            stat[i] = (4, switcht , tp[2], tptau)
                            nextel = readyq.get()
                            tp = stat[nextel[1]]
                            swchnum = nextel[1]
                            waitt = waitt + tp[1] * -1
                            stat[nextel[1]] = (4, switcht, tp[2], tp[3])
                        if tmln < 1000:
                            print('time {}ms: Process {} switching out of CPU;'.format(tmln, processlist[i]), end='')
                            print(' will block on I/O until time {}ms '
                                  .format(data[i][stat[i][2]][1] + tmln+int(switcht/timediv)), end='')
                            print_q(i, tmln, readyq)
                        # print(len(readyq.queue))


                        # stat[nextel[1]][1] = data[nextel[1]][stat[nextel[1]][2]][0]
                else:  # switched, start cpu

                    # print("switch triggered")
                    if swchnum == i:  # from switch to cpu
                        running = i
                        swchc = swchc + 1
                        # nextel = readyq.get()
                        running = i
                        # print("hakjshdkjahskjdh")
                        tp = stat[i]
                        waitt = waitt + tp[1] * -1
                        if (remain[i] == -1):
                            ccpu = ccpu + 1
                            ttcpu = ttcpu + data[i][stat[i][2]][0]
                            stat[i] = (3, data[i][stat[i][2]][0], tp[2], tp[3])
                        else:
                            swchc = swchc + 1
                            stat[i] = (3, remain[i], tp[2], tp[3])
                        running = i
                        if tmln < 1000:
                            print('time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst'
                                  .format(tmln, processlist[i], stat[i][3], stat[i][1]), end='')
                            print_q(i, tmln, readyq)
                    else:  # from switch to queue or io

                        if (swchto == 'io'):
                            # print(data[i][stat[i][2]][1], "what is happening")
                            tp = stat[i]
                            stat[i] = (1, data[i][stat[i][2]][1], tp[2], tp[3])

                        else:
                            tp = stat[i]
                            waitt = waitt + tp[1] * -1
                            stat[i] = (2, -1, tp[2], tp[3])
                            readyq.put((tp[3], i))
            tp = stat[i]
            stat[i] = (tp[0], tp[1] - 1, tp[2], tp[3])
            # if tmln < 1000:
            #     print(stat)
        tmln = tmln + 1
        if (tmln > 5000):
            break
    ttt = 0
    for i in range(len(stat)):
        ttt = ttt + stat[i][1]
    print("time {}ms: Simulator ended for SJF [Q <empty>]".format(tmln))
    # print("-- average CPU burst time:", ttcpu / ccpu, "ms")
    # print("-- average wait time:", waitt / waitc, "ms")
    # print("-- average turnaround time: {:.3f}".format(ttt / bursc))
    # print("-- total number of context switches:", swchc)
    # print("-- total number of preemptions:", preec)
    return ttcpu / ccpu, waitt / waitc, ttt / bursc, swchc,preec




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


def SRT(data, alpha,lmda,switcht, processlist):
    ttcpu = 1
    ccpu = 1
    waitt = 1
    waitc = 1
    swchc = 1
    preec = 1
    swching = False
    remain = []
    print(switcht)
    arrivq = PriorityQueue()
    readyq = PriorityQueue()
    stat = []
    tau = 1/lmda
    t = 10
    swchto = 'n'
    swchnum = -1
    running = -1
    finished = 0
    preem = False
    bursc = 0
    for i in range(len(data)):
        stat.append((0, data[i]["arrival"], -1, tau))
        remain.append(-1)
        print('Process',processlist[i],"[NEW] (arrival time",stat[i][1],"ms)",len(data[i])-1,'CPU bursts' )
        bursc = bursc + len(data[i])-1

    tmln = 0
    print('time 0ms: Simulator started for SRT [Q <empty>]')
    while max(stat)[0] != -1:

        # print(tmln,"new")
        # print(remain)
        for i in range(len(data)):
            # print(swchnum)
            #print(stat, i)
            if stat[i][0] == -1:
                continue
            # if tmln > 310 and tmln < 450:
            #     print(stat[i][0], running )
            if stat[i][0] ==2 and running == -2:
                if len(readyq.queue) != 0:
                    running = i
                    # print('very not ', processlist[i])
                    swchnum = i
                    tp = stat[i]
                    remain[i] = -1
                    readyq.get()
                    readyq.put((0,i))

                    # print(readyq.queue)
                    waitt = waitt + tp[1]*-1
                    stat[i] = (4, switcht/2 - 1, tp[2], tp[3])


            if stat[i][1] == 0:#something's happening
                #print("not rifhgt")
                if stat[i][0] == 0:#arrived and queuing
                    #stat[i][2] = stat[i][2] + 1
                    #cput = data[i][stat[i][2]][0]
                    tp = stat[i]

                    stat[i] = (2,tp[1],tp[2]+1,tp[3])
                    readyq.put((tau, i))
                    print('time {}ms: Process {} (tau {}ms) arrived; added to ready queue '.format(tmln, processlist[i], stat[i][3]),
                          end='')
                    print_q(i,tmln,readyq)
                    if swchnum == -1:#first CPU use
                        tp = stat[i]
                        # readyq.get()
                        swchnum = i
                        stat[i] = (4,switcht/2,tp[2], tp[3])

                    elif (stat[running][1] > stat[i][3]):
                        #print(123123123)
                        swchto = 'q'
                        swchnum = i

                        stat[i] = (4, switcht, tp[2] + 1, tp[3])
                        tp = stat[running]
                        preem = True
                        remain[running] = tp[1]
                        stat[running] = (4, switcht, tp[2], tp[3])
                        running = i
                    elif (stat[running][1] == stat[i][3]):
                        pr = handleTies(running,i)
                        if i != pr:
                            pn = i
                        else:
                            pn = running
                        if running == pr:

                            stat[i] = (2, -1, tp[2] + 1, tp[3])
                            readyq.put((stat[i][3], i))

                        else:
                            swchto = 'q'
                            swchnum = pr
                            tp = stat[pr]
                            waitt = waitt + tp[1] * -1
                            remain[running] = stat[running][1]
                            stat[pr] = (4, switcht,tp[2]+1,tp[3])
                            tp = stat[running]
                            preem = True
                            stat[running] = (4,switcht,tp[2],tp[3])
                            running = pr

                elif stat[i][0] == 1:#io'ed to ready queue
                    tp = stat[i]
                    # print('real trying to switch')
                    #print(stat[running][1] , stat[i][3])
                    # print(99)
                    waitc = waitc + 1
                    stat[i] = (2, -1, tp[2] + 1, tp[3])
                    readyq.put((stat[i][3], i))
                    # if stat[i][0] == 2 and running == -2:
                    #     if len(readyq.queue) != 0:
                    #         running = i
                    #         print('very not ', processlist[i])
                    #         swchnum = i
                    #         tp = stat[i]
                    #         remain[i] = -1
                    #         readyq.get()
                    #         readyq.put((0, i))
                    #
                    #         print(readyq.queue)
                    #         waitt = waitt + tp[1] * -1
                    #         stat[i] = (4, switcht / 2 - 1, tp[2], tp[3])
                    if (running >= 0 and stat[running][1] > stat[i][3] and not swching):
                        # print(11)
                        swchto = 'q'
                        swchnum = i
                        # readyq.put((stat[running][3], running))
                        if tmln < 1000:
                            print(
                                "time {}ms: Process {} (tau {}ms) completed I/O;".format(tmln, processlist[i], stat[i][3]),
                                end='')
                            print(' preempting {} '.format(processlist[running]), end='')
                            print_q(i, tmln, readyq)
                        waitt = waitt + tp[1] * -1
                        stat[i] = (4, switcht, tp[2] + 1, tp[3])
                        tp = stat[running]

                        remain[running] = tp[1]
                        preem = True
                        stat[running] = (4, switcht/2 , tp[2], tp[3])
                        running = i
                    elif (running >= 0 and stat[running][1] == stat[i][3] and not swching):
                        # print(13)
                        pr = handleTies(running,i)
                        if i != pr:
                            pn = i
                        else:
                            pn = running
                        if running == pr:

                            stat[i] = (2, -1, tp[2] + 1, tp[3])
                            readyq.put((stat[i][3], i))
                            continue
                        if tmln < 1000:
                            print(
                                "time {}ms: Process {} (tau {}ms) completed I/O;".format(tmln, processlist[i], stat[i][3]),
                                end='')
                            print(' preempting {} '.format(running), end='')
                            print_q(i, tmln, readyq)
                        swchto = 'q'
                        swchnum = pr
                        tp = stat[pr]
                        waitt = waitt + tp[1]*-1
                        stat[pr] = (4, switcht,tp[2]+1,tp[3])
                        tp = stat[running]
                        preem = True
                        remain[running] = tp[1]
                        stat[running] = (4,switcht,tp[2],tp[3])
                        running = pr
                        if tmln < 1000:
                            print(
                                "time {}ms: Process {} (tau {}ms) completed I/O;".format(tmln, processlist[i], stat[i][3]),
                                end='')
                            print(' preempting {} '.format(), end='')
                            print_q(i, tmln, readyq)
                    else:

                        if tmln < 1000:
                            print(
                                "time {}ms: Process {} (tau {}ms) completed I/O;".format(tmln, processlist[i], stat[i][3]),
                                end='')
                            print('added to ready queue ', end='')
                            print_q(i, tmln, readyq)

                elif stat[i][0] == 3:#finished running, to next
                    running = -2
                    #stat[i][4] = t * alpha + (1 - alpha) * stat[i][4]
                    # print("in running")
                    preem = False
                    tptau = stat[i][3] * alpha + (1 - alpha) * data[i][stat[i][2]][0]
                    tptau = math.ceil(tptau)
                    if tmln < 1000:
                        print(
                            'time {}ms: Process {} (tau {}ms) completed a CPU burst;'.format(tmln, processlist[i],
                                                                                             stat[i][3]),
                            end='')
                        print(' {} bursts to go '.format(len(data[i]) - stat[i][2] - 2), end='')
                        print_q(i, tmln, readyq)
                        print(
                            'time {}ms: Recalculated tau = {}ms for process {} '.format(tmln, tptau, processlist[i], ),
                            end='')
                        print_q(i, tmln, readyq)
                    if len(readyq.queue) == 0 and data[i][stat[i][2]][1] != 0 and len(stat) != 1:
                        # print('1123123123',finished)
                        # if finished == len(stat) - 1:
                        if tmln < 1000:
                            print(
                                'time {}ms: Process {} switching out of CPU;'.format(tmln, processlist[i]),
                                end='')
                            print(' will block on I/O until time {}ms '.format(data[i][stat[i][2]][1] + tmln+switcht/2), end='')
                            print_q(i, tmln, readyq)
                        # print(data[i][stat[i][2]])
                        tp = stat[i]
                        swchto = 'io'
                        swchnum = -1
                        running = -2
                        stat[i] = (4, switcht/2, tp[2], tptau)

                        if data[i][stat[i][2]][1] == 0:
                            #print('1')
                            tp = stat[i]
                            stat[i] = (-1, tmln - data[i]["arrival"], tp[2], tptau)
                            finished = finished + 1
                        #continue
                    # else:
                    #     continue


                    elif data[i][stat[i][2]][1] == 0:#finished
                        # print('2',finished)
                        if(finished == len(stat)):
                            ttt = 0
                            for i in range(len(stat)):
                                ttt = ttt + stat[i][1]
                            print("time {}ms: Simulator ended for SRT [Q <empty>]".format(tmln))
                            # print("-- average CPU burst time:", ttcpu/ccpu,"ms")
                            # print("-- average wait time:", waitt /waitc, "ms")
                            # print("-- average turnaround time: {:.3f}".format(ttt/bursc))
                            # print("-- total number of context switches:",swchc)
                            # print("-- total number of preemptions:", preec)
                            return ttcpu / ccpu, waitt / waitc, ttt / bursc, swchc, preec
                        tp = stat[i]
                        stat[i] = (-1,tmln - data[i]["arrival"], tp[2],tptau)
                        finished = finished +1
                        if tmln < 1000:

                            print(
                                'time {}ms: Process {} (tau {}ms) completed a CPU burst;'.format(tmln, processlist[i], stat[i][3]),
                                end='')
                            print(' {} bursts to go '.format(0), end='')
                            print_q(i, tmln, readyq)
                        if len(readyq.queue) == 0:
                            tp = stat[i]
                            stat[i] = (tp[0], tp[1] - 1, tp[2], tptau)
                            continue
                        nextel = readyq.queue[0]
                        tp = stat[nextel[1]]
                        waitt = waitt + tp[1] * -1
                        stat[nextel[1]] = (4,switcht,tp[2],tp[3])
                        swchnum = nextel[1]

                    else: #to next
                        # print('3')
                        tp = stat[i]
                        stat[i] = (4, switcht/2, tp[2],tptau)
                        swchto = 'io'
                        swchnum = -1
                        timediv = 2
                        if len(readyq.queue) >= 1:
                            # print("asdasdasd")
                            timediv = 1
                            stat[i] = (4, switcht/2, tp[2], tptau)
                            nextel = readyq.queue[0]
                            swchnum = nextel[1]
                            # print(swchnum)
                            tp = stat[nextel[1]]
                            waitt = waitt + tp[1] * -1
                            stat[nextel[1]] = (4, switcht, tp[2], tp[3])
                            swching = True

                        if tmln < 1000:
                            print(
                                'time {}ms: Process {} switching out of CPU;'.format(tmln, processlist[i]),
                                end='')
                            print(' will block on I/O until time {}ms '.format(data[i][stat[i][2]][1]+tmln+ int(switcht/2)),end='')
                            print_q(i, tmln, readyq)



                        # stat[nextel[1]][1] = data[nextel[1]][stat[nextel[1]][2]][0]
                else:#switched, start cpu
                    # print("switch triggered")
                    if swchnum == i:#from switch to cpu
                        running = i
                        #nextel = readyq.get()
                        running = i
                        # print("hakjshdkjahskjdh", preem)
                        readyq.get()
                        tp = stat[i]
                        if(preem):
                            preec = preec + 1
                        else:
                            swchc = swchc + 1

                        if( remain[i] == -1 and not preem):
                            # print(13333,i)
                            ttcpu = ttcpu + data[i][stat[i][2]][0]
                            ccpu = ccpu +1
                            stat[i] = (3,data[i][stat[i][2]][0], tp[2], tp[3] )
                        else:
                            if remain[i] == -1 :
                                ttcpu = ttcpu + data[i][stat[i][2]][0]
                                ccpu = ccpu + 1
                                stat[i] = (3, data[i][stat[i][2]][0], tp[2], tp[3])
                            else:
                                # print(22222)
                                stat[i] = (3, remain[i], tp[2], tp[3])
                        running = i
                        if tmln < 1000:
                            print('time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst remaining '.format(tmln,
                                                                                                                processlist[
                                                                                                                    i],
                                                                                                                stat[i][
                                                                                                                    3],
                                                                                                                stat[i][
                                                                                                                    1]),
                                  end='')
                            print_q(i, tmln, readyq)

                    else:#from switch to queue or io
                        # print(i,"what is happening")
                        if(swchto == 'io'):
                            # print(88888,data[i])
                            tp = stat[i]
                            stat[i] = (1, data[i][stat[i][2]][1], tp[2], tp[3])
                        else:
                            # print(99999)
                            tp = stat[i]
                            stat[i] = (2, -1, tp[2], tp[3])
                            readyq.put((tp[3],i))

                if not preem and len(readyq.queue) != 0:

                    if (running >= 0 and stat[running][3] > stat[readyq.queue[0][1]][3] and running != readyq.queue[0][1]):
                        # print(11)
                        preem = True
                        swchto = 'q'
                        swchnum = readyq.queue[0][1]
                        tp = stat[readyq.queue[0][1]]
                        # readyq.put((stat[running][3], running))
                        if tmln < 1000:
                            print(
                                "time {}ms: Process {} (tau {}ms)".format(tmln, processlist[readyq.queue[0][1]],
                                                                                         stat[readyq.queue[0][1]][3]),
                                end='')
                            print(' will preempt {} '.format(processlist[running]), end='')
                            print_q(readyq.queue[0][1], tmln, readyq)
                        waitt = waitt + tp[1] * -1
                        stat[readyq.queue[0][1]] = (4, switcht - 1, tp[2] , tp[3])
                        tp = stat[running]
                        # print(tp)
                        remain[running] = tp[1]
                        preem = True
                        stat[running] = (4, switcht / 2 -1, tp[2], tp[3])
                        running = readyq.queue[0][1]
                if stat[i][0] == 2 and running == -2:
                    if len(readyq.queue) != 0:
                        running = i
                        # print('very not ', processlist[i])
                        swchnum = i
                        tp = stat[i]
                        remain[i] = -1
                        readyq.get()
                        readyq.put((0, i))

                        # print(readyq.queue)
                        waitt = waitt + tp[1] * -1
                        stat[i] = (4, switcht / 2, tp[2], tp[3])
            tp = stat[i]
            stat[i] = (tp[0], tp[1] - 1, tp[2], tp[3])
            # if tmln < 400:
                # print(stat)
        tmln = tmln + 1
        if(tmln > 5100):
            break
    ttt = 0
    for i in range(len(stat)):
        ttt = ttt+stat[i][1]
    print("time {}ms: Simulator ended for SRT [Q <empty>]".format(tmln))
    # print("-- average CPU burst time:", ttcpu/ccpu,"ms")
    # print("-- average wait time:", waitt /waitc, "ms")
    # print("-- average turnaround time: {:.3f}".format(ttt/bursc))
    # print("-- total number of context switches:",swchc)
    # print("-- total number of preemptions:", preec)
    return ttcpu / ccpu, waitt / waitc, ttt / bursc, swchc,preec

