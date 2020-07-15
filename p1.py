import sys


def drand48(seed):
  a = 273673163155
  c = 138
  m = 281474976710656
  seed = (a * seed + c) % m
  print(seed)
  # return ??? <- find what to return



if __name__ == '__main__':
  print("This is OPSYS project")
  drand48(1000)
  print("xuchang")
  print("Hello!")
  print(sys.argv)