import sys


def drand48(seed):
  a = 273673163155
  c = 138
  m = 281474976710656
  seed = (a * seed + c) % m
  print(seed)
  # return ??? <- find what to return

  # class Rand48(object):
  #   def __init__(self, seed):
  #     self.n = seed
  #
  #   def seed(self, seed):
  #     self.n = seed
  #
  #   def srand(self, seed):
  #     self.n = (seed << 16) + 0x330e
  #
  #   def next(self):
  #     self.n = (25214903917 * self.n + 11) & (2 ** 48 - 1)
  #     return self.n
  #
  #   def drand(self):
  #     return self.next() / 2 ** 48
  #
  #   def lrand(self):
  #     return self.next() >> 17
  #
  #   def mrand(self):
  #     n = self.next() >> 16
  #     if n & (1 << 31):
  #       n -= 1 << 32
  #     return n


if __name__ == '__main__':
  process = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
             "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
  drand48(1000)
  print("HelloWorld!")
  print(sys.argv)