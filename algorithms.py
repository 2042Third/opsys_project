import sys

'''
param: list data, data = [{arrival: t, cpuburst: t, ioburst: t},{}...]
effects: none
returns: none
Note: Simulates first-come-first-serve modal in CPU scheduling. 
        Assuming data[0] is process 'A', and data[1] is process 'B', and so on.
'''


def FCFS(data):
    return 0


def SJF():
    return 0


def SRT():
    return 0


'''
param: list data, t, bne, data = [{arrival: t, cpuburst: t, ioburst: t},{}...],
 t = time slice, bne = beginning or end of the sequence
effects: none
returns: none
Note: Simulates Round-Robin modal in CPU scheduling. 
        Assuming data[0] is process 'A', and data[1] is process 'B', and so on.
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
