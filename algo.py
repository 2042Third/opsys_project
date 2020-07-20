import sys
import math
from queue import PriorityQueue
# from p1 import handleTies

class Board:
    time = -1
    buff = 0
    norbuff = 0
    preems = []
    rdn = 1000
    preempyyy = 0.0
    switches = 0.0
    wait = 0.0
    waitc = 0.0
    waitq = dict()
    def __init__(self, switcht, alpha, process, data ):
        self.cpu = [0,0,0]#stat,time,proc
        self.pcb = [0,0,0,0,0,0]#stat,time,proc1,proc2,to,come
        self.process = process
        self.readyq = PriorityQueue()
        self.io = []
        self.data = data
        self.switcht = switcht
        self.alpha = alpha

    def gt(self):
        return self.time+1



    def trycpu(self, proc):#not finished
        if self.cpu[0] == 0 and self.pcb[0] == 0 and len(self.readyq.queue) != 0:

            self.pcbcpu(proc)
            return True
        return False

    def endtrycpu(self, proc):#not finished
        if self.cpu[0] == 0 and self.pcb[0] == 0 and len(self.readyq.queue) != 0:

            self.endpcbcpu(proc)
            return True
        return False

    def stattrycpu(self):
        if self.cpu[0] == 0 and self.pcb[0] == 0 and len(self.readyq.queue) != 0:

            # self.pcbcpu(proc)
            return True
        return False

    def upcpu(self):

        if self.cpu[1] == 0 and self.cpu[0] == 1:

            self.cpu[0] = 0
            if self.cpu[2].cpucheckfini():

                print('time {}ms: Process {} terminated '.format(self.gt(),self.cpu[2].getna()),end='')
                self.rdqprint()

                return
            self.pcbio()

            if self.time < self.rdn:
                print('time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go '.format(self.gt(),self.cpu[2].getna(),self.cpu[2].gettau(), self.cpu[2].remburs()-3),end='')
                self.rdqprint()
            self.cpu[2].taup(self.cpu[2].getcpt())
            if self.time < self.rdn:
                print('time {}ms: Recalculated tau = {}ms for process {} '.format(self.gt(),self.cpu[2].gettau(),self.cpu[2].getna()), end='')
                self.rdqprint()
                print('time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms '.format(self.gt(),
                                                                                  self.cpu[2].getna(), int(self.cpu[2].getiot()+self.switcht/2+self.gt())), end='')
                self.rdqprint()
            if len(self.readyq.queue) != 0:
                if self.trycpu(self.rdqsee()):
                    self.rdqget()
            if len(self.readyq.queue) != 0 :
                if self.cpu[2].getnum() != self.rdqsee()[1]:
                    tp = self.rdqget()
                    self.pcbiocpu(self.data[tp[1]])
                else:
                    tp = self.rdqget()
                    self.pcbio()


    def upt(self):
        for i in range(len(self.io)):
            self.io[i].upt()
        if self.cpu[1] != 0:
            self.cpu[1] -= 1
            self.cpu[1] =int(self.cpu[1])
        if self.pcb[1] != 0:
            # print('pcb',self.pcb)
            self.pcb[1] -= 1
            self.pcb[1] = int(self.pcb[1])
        for key in self.waitq:
            # print('dict,', key, self.waitq[key])
            self.waitq[key] += 1

        self.time += 1

    def getreturn(self):
        return self.wait/self.waitc , self.switches, self.preempyyy

    def upio(self):
        tmp = []
        for i in range(len(self.io)):

            if self.io[i].gt() == 0:
                self.io[i].toio()

                self.rdqadd(self.io[i])
                tmp.append(i)
                if self.time < self.rdn:
                    print('time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue '.format(self.gt(),
                                                                                                         self.io[i].getna(),
                                                                                                         self.io[
                                                                                                             i].gettau(), ),
                          end='')
                    self.rdqprint()
            if self.trycpu(self.io[i]):
                self.rdqget()
        for i in tmp:
            del self.io[i]



    def rdqprint(self):
        print("[Q", end='')
        if len(self.readyq.queue) == 0:
            print(" <empty>]")
        else:
            for z in range(len(self.readyq.queue)):
                print(" {}".format(self.process[self.readyq.queue[z][1]]), end="")
            print(']')

    def rdqadd(self,proc):
        proc.tord()
        if self.cpu[0] == 1 or self.cpu[0] == 2:
            tmp = self.preemp(self.cpu[2], proc)
            if tmp:
                if tmp == 111:
                    self.preems.append(proc)
                return
            elif not proc in list(self.readyq.queue):
                proc.tord()
                self.waitc = self.waitc + 1.0
                self.waitq[proc.getna()] = 0

                self.readyq.put((proc.gettau(), proc.getnum()))
        elif not proc in list(self.readyq.queue):
            proc.tord()
            self.waitc = self.waitc + 1.0
            self.waitq[proc.getna()] = 0
            self.wait += self.waitq[proc.getna()]
            # print('aa',self.wait)
            self.readyq.put((proc.gettau(),proc.getnum()))

    def rdqget(self):
        # print( self.process[self.rdqsee()[1]])
        self.wait += self.waitq[self.process[self.rdqsee()[1]]]
        return self.readyq.get()

    def rdqsee(self):
        return self.readyq.queue[0]

    def pcbrd(self):
        self.cpu[2].sett(-1)
        self.cpu[0] = 2
        self.cpu[2].setrem(self.cpu[1])
        self.pcb[0] = 1
        self.pcb[1] = self.switcht/2
        self.pcb[2] = self.cpu[2].topcb()
        # self.pcb[3] = 0
        self.pcb[4] = 'rd'

    def pcbio(self):
        self.cpu[2].sett(-1)
        self.cpu[0] = 2
        self.cpu[2].setrem(self.cpu[1])
        self.pcb[0] = 1
        self.pcb[1] = self.switcht/2
        self.pcb[2] = self.cpu[2].topcb()
        # self.pcb[3] = 0
        self.pcb[4] = 'io'

    def pcbiocpu(self, proc):
        self.cpu[2].sett(-1)
        proc.sett(-1)

        self.cpu[0] = 2
        self.cpu[2].setrem(self.cpu[1])
        self.pcb[0] = 2
        self.pcb[1] = self.switcht
        self.pcb[2] = self.cpu[2].topcb()
        self.pcb[3] = proc.topcb()
        self.pcb[4] = 'io'
        self.pcb[5] = 'cpu'


    def pcbrdcpu(self, proc):
        self.cpu[2].sett(-1)
        proc.sett(-1)
        self.cpu[0] = 2
        self.cpu[2].setrem(self.cpu[1])
        self.pcb[0] = 2
        self.pcb[1] = self.switcht
        self.pcb[2] = self.cpu[2]
        self.pcb[3] = proc.topcb()
        self.pcb[4] = 'rd'
        self.pcb[5] = 'cpu'

    def endpcbcpu(self,proc):
        proc.sett(-1)
        self.cpu[0] = 2
        self.cpu[2] = proc
        self.pcb[0] = 1
        # print("-----------------------------------------------------------------------------------------")
        self.pcb[1] = self.switcht
        self.pcb[2] = proc.topcb()
        self.pcb[4] = 'cpu'

    def pcbcpu(self,proc):
        proc.sett(-1)
        self.cpu[0] = 2
        self.cpu[2] = proc
        self.pcb[0] = 1
        # print("-----------------------------------------------------------------------------------------")
        self.pcb[1] = self.switcht/2
        self.pcb[2] = proc.topcb()
        self.pcb[4] = 'cpu'

    def uppcb(self):#updates pcb proccesses
        if self.pcb[0] == 1:
            if self.pcb[1] == 0:
                self.switches = self.switches + 1.0
                if self.pcb[4] == 'io':
                    self.cpu[0] = 0
                    self.pcb[2].setrem(0)
                    self.pcb[2].toio()
                    self.io.append(self.pcb[2])
                    self.pcb[0] = 0
                elif self.pcb[4] == 'cpu':

                    self.cpu[0] = 1
                    self.cpu[1] = self.pcb[2].tocpu()
                    self.cpu[2] = self.pcb[2]
                    if self.time < self.rdn:
                        print('time {}ms: Process {} (tau {}ms) started using the CPU with {}ms burst remaining '.format(self.gt(),self.cpu[2].getna(),self.cpu[2].gettau(),self.cpu[1]),end='')
                        self.rdqprint()
                    # self.rdqget()
                    self.pcb[0] = 0
                    if len(self.preems) != 0:
                        b = self.preems[0]
                        if self.time < self.rdn:

                            print("time {}ms: Process {} (tau {}ms) will preempt {} ".format(self.time+1, b.getna(), b.gettau(),self.cpu[2].getna()))
                            self.rdqprint()
                        self.preempyyy += 1
                        self.pcbrdcpu(b)
                        del self.preems[0]
                    # if (self.pcb[0] == 1 and self.pcb[2].getstat() == "cua"):
                    #     self.pcbiocpu(self.buff)
                    #     buff = 0
                elif self.pcb[4] == 'rd':

                    self.pcb[2].tord()
                    self.rdqadd(self.pcb[2])
                    self.pcb[0] = 0
        elif self.pcb[0] == 2:

            self.switches = self.switches + 1.0
            if self.pcb[1] == self.switcht /2:
                if self.pcb[4] == 'io':
                    self.pcb[2].setrem(0)
                    self.pcb[2].toio()
                    self.io.append(self.pcb[2])
                # elif self.pcb[4] == 'cpu':
                #     # self.rdqget()
                #
                #     self.pcb[2].setrem(0)
                #     self.cpu[0] = 1
                #     self.cpu[1] = self.pcb[2].tocpu()
                #     self.cpu[2] = self.pcb[2]
                #     print('time {}ms: Process {} (tau {}ms) started using the CPU with {}ms burst remaining '.format(
                #         self.gt(), self.cpu[2].getna(), self.cpu[2].gettau(), self.cpu[1]), end='')
                #     self.rdqprint()
                elif self.pcb[4] == 'rd':
                    self.pcb[2].tord()
                    self.rdqadd(self.pcb[2])
            if self.pcb[1] == 0:
                # if self.pcb[5] == 'io':
                #     self.pcb[2].setrem(0)
                #     self.pcb[2].toio()
                #     self.io.append(self.pcb[2])
                #     self.pcb[0] = 0
                if self.pcb[5] == 'cpu':
                    # self.rdqget()

                    # self.pcb[3].setrem(0)
                    self.cpu[0] = 1
                    self.cpu[1] = self.pcb[3].tocpu()
                    self.cpu[2] = self.pcb[3]
                    self.pcb[0] = 0
                    if self.time < self.rdn:
                        print('time {}ms: Process {} (tau {}ms) started using the CPU with {}ms burst remaining '.format(
                            self.gt(), self.cpu[2].getna(), self.cpu[2].gettau(), self.cpu[1]), end='')
                        self.rdqprint()

                # elif self.pcb[5] == 'rd':
                #     self.pcb[2].tord()
                #     self.rdqadd(self.pcb[2])
                #     self.pcb[0] = 0



    def preemp(self, a, b):#not finished
        # print('this i s',a, b)
        anum = 0
        bnum = 0
        if a.getstat() == 'cpu' :
            anum = a.getcpt() - self.cpu[1]
        if b.getstat() == 'cpu' and b.getrem() != 0:
            bnum = b.getcpt() - b.getrem()
        anum =  a.gettau() - anum
        bnum = b.gettau() - bnum

        if anum > bnum :
            self.buff = b
            if a.getstat() == 'cpu' and self.cpu[1] >= 0:
                if b.getstat() == 'rd':
                    self.pcbrdcpu(b)
                    if self.time < self.rdn:
                        print("time {}ms: Process {} (tau {}ms) completed I/O; preempting {} ".format(self.time+1, b.getna(), b.gettau(),a.getna()))
                    self.preempyyy += 1
                    return True
            elif self.pcb[4] == 'cpu' and a.gett() < 0:
                if b.getstat() == 'rd':
                    b.setcua()
                    # if self.time < 1000:
                        # print("time {}ms: Process {} (tau {}ms) completed I/O; will preempt {} ".format(self.time+1, b.getna(), b.gettau(),a.getna()))
                    return 111
        elif anum == bnum and b.getna() < a.getna():
            self.buff = b
            if a.getstat() == 'cpu' and a.gett() >= 0:
                if b.stat() == 'rd':
                    self.pcbrdcpu(b)
                    self.preemp += 1
                    if self.time < self.rdn:

                        print("time {}ms: Process {} (tau {}ms) completed I/O; preempting {} ".format(self.time+1,
                                                                                                      b.getna(),
                                                                                                      b.gettau(),
                                                                                                      a.getna()))
                    return True
            elif a.getstat() == 'cpu' and a.gett() >= -1:
                if b.getstat() == 'rd':
                    b.setcua()
                    # if self.time < 1000:
                        # print("time {}ms: Process {} (tau {}ms) completed I/O; will preempt {} ".format(self.time+1,
                        #                                                                                 b.getna(),
                        #                                                                                 b.gettau(),
                        #                                                                                 a.getna()))
                    return 111
        return False

class Proc:
    time = 0
    finished = False
    def __init__(self, name, arriv, bursts, tau, alpha,process):
        self.stat = 0
        self.name = name
        self.arriv = arriv
        self.burs = bursts
        self.tau = int(tau)
        self.remain = 0
        self.cpio = 0
        self.bursc = -1
        self.alpha = alpha
        self.time = arriv
        self.process = process
        print("Process {} [NEW] (arrival time {} ms) {} CPU bursts (tau {}ms)".format(process[name], arriv, len(bursts)-1,self.tau))

    def getstat(self):
        a = self.stat
        if a == 0:
            return 0
        elif a == 1:
            return 'cpu'
        elif a == 2:
            return 'pcb'
        elif a == 3:
            return 'io'
        elif a == 4:
            return 'rd'
        else:
            return self.stat
    def gett(self):
        return self.time

    def remburs(self):
        return int(len(self.burs) - self.bursc+1)

    def fini(self):
        return self.finished

    def cpucheckfini(self):
        if self.burs[self.bursc][1] == 0:
            self.finished = True
            self.stat = -2
            return True
        return False

    def getcpt(self):
        return self.burs[self.bursc][0]

    def getiot(self):
        return self.burs[self.bursc][1]

    def arv(self):#

        if self.stat == 0:
            if self.time == 0:
                self.stat = -1
                return True
        return False

    def setcua(self):
        self.stat = 'cua' # change upon arrival

    def getna(self):
        return self.process[self.name]

    def gettau(self):
        return int(self.tau)

    def taup(self, t):
        # print('')
        self.tau = self.tau * self.alpha + (1 - self.alpha) * t
        self.tau = math.ceil(self.tau)




    def setrem(self,rem):
        self.remain = rem

    def getrem(self):
        return self.remain

    def sett(self,tt):
        self.time = tt

    def gt(self):
        return self.time

    def toio(self):
        self.cpio = 1
        self.stat = 3
        self.sett(self.burs[self.bursc][1])
        if self.time == 0:
            self.finished = True
            self.stat = -2
        return self.burs[self.bursc][1]

    def tord(self):
        self.stat = 4


    def tocpu(self):
        self.cpio = 0
        self.stat = 1
        if self.remain == 0:
            self.bursc += 1
            return self.burs[self.bursc][0]
        else:
            return self.remain

    def topcb(self):

        return self

    def getnum(self):
        return self.name

    def debug(self):
        print('name={} time={} stat={} tau={} rem={} bursc={} cpio={} '.format(self.getna(),self.gt(),self.getstat(),self.gettau(),self.remain,self.bursc,self.cpio))

    def upt(self):
        if self.time != 0:
            self.time -= 1
        return self.time

def SRT2(data, alpha,lmda,switcht, processlist, cal):

    procs = []
    finishedprocs = []
    # print("time 0ms: Simulator started for SRT [Q <empty>]")
    for i in range(len(data)):
        # print(processlist)
        procs.append(Proc(i,data[i]['arrival'],data[i],1/lmda,alpha, processlist))
    mbd = Board(switcht, alpha, processlist, procs)
    finishnum = 0
    print("time 0ms: Simulator started for SRT [Q <empty>]")
    while finishnum != len(data):
        finishnum = 0
        mbd.upt()
        mbd.uppcb()
        mbd.upcpu()
        mbd.upio()

        # print('time {}ms: '.format(mbd.gt() ), end='')
        # mbd.rdqprint()
        needtry = False
        needtrynum = -1
        for i in range(len(data)):
            if finishnum!=0 and procs[needtrynum].cpio == True:
                needtry = False
                procs[needtrynum].cpio = False
                # print('whatasdasdasdasda')
                if len(mbd.readyq.queue) != 0:
                    mbd.endtrycpu(procs[mbd.readyq.queue[0][1]])
            if procs[i].fini():
                finishnum += 1
                if mbd.cpu[0] == 0:
                    if len(mbd.readyq.queue) != 0:
                        if mbd.stattrycpu():
                            needtry = True
                        if procs[i].cpio != -2 :
                            procs[i].cpio = True
                            needtrynum = i
                # if mbd.gt() <2720:
                #     print(finishnum)
                continue
            # print(procs[i].gt(), procs[i].getna())
            if procs[i].getstat() == 0:
                # print('a')
                procs[i].upt()

            if procs[i].arv():
                mbd.rdqadd(procs[i])
                print('time {}ms: Process {} (tau {}ms) arrived; added to ready queue '.format(mbd.gt(), procs[i].getna(),procs[i].gettau(),),end='')
                mbd.rdqprint()

                if mbd.trycpu(procs[i]):
                    mbd.rdqget()
            # else:
            #     if mbd.trycpu(procs[i]):
            #         mbd.rdqget()
        # if mbd.gt() < 3250 :
        #     print('-----------------------------------------------cpu',mbd.gt(),mbd.cpu)
        #     print('-----------------------------------------------pcb',mbd.pcb)
        #     print('-----------------------------------------------',end='')
        #     print(procs[0].debug())
        #     print('-----------------------------------------------',end='')
        #     print(procs[1].debug())
        # if mbd.gt() > 5500:
        #     print("debug",mbd.gt())
        #     break
    print("time {}ms: Simulator ended for SRT [Q <empty>]".format(mbd.gt()+2))
    tmpa = mbd.getreturn()
    bursts = 0
    avgsw = mbd.wait/mbd.waitc
    for i in procs:
        bursts += (len(i.burs)-1)
    # print(tmpa[2])
    avgtrn = cal + avgsw
    avgtrn +=  switcht/2 * tmpa[2]/bursts
    return cal,tmpa[0],avgtrn,tmpa[1],tmpa[2]

