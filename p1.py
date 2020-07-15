import sys

def drand48(seed):
  a = 273673163155
  c = 138
  m = 281474976710656
  seed = (a * seed + c) % m
  print(seed)
  return seed



# generate the processes
# n: the number of process generates (1<=n<=26)
# using the drand() to identify the number of bursts time; using the exp-random to identify the cpu and I/O burst time
def processGen(n):
  return 1



if __name__ == '__main__':
# get all the cmd/parameters
#  n = int(sys.argv[1])
#  seed = int(sys.argv[2])
#  Lambda = float(sys.argv[3])
#  upperbound = int(sys.argv[4])
#  t_cs  = int(sys.argv[5])
#  alpha = float(sys.argv[6])

  print("test", drand48(12) % 10)