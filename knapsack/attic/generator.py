import sys
import random 
import argparse


def add_case(n, x, a):
    assert 1 <= n <= 1e5
    assert 1 <= x <= 1e9
    assert len(a) == n
    assert 1 <= min(a) and max(a) <= 1e9
    return str(n)+" "+str(x)+"\n"+' '.join(map(str, a))

random.seed(str(sys.argv[1]))

mode = sys.argv[2]
n = int(sys.argv[3])
maxval = int(sys.argv[4])
x = 0
a = []

if mode == "small":
  x = maxval
  maxa = x // n // 2
  a = [random.randint(1, maxa) for _ in range(n)]

elif mode == "big":
  maxa = maxval
  x = random.randint(1, maxa-1)
  a = [random.randint(x+1, maxa) for _ in range(n)]

elif mode == "small_big":
  maxa = maxval
  x = maxval // 2
  m = random.randint(1, n);
  a = [random.randint(1, x // m // 2) for _ in range(m)] + [random.randint(x+1, maxa) for _ in range(n-m)]
  random.shuffle(a)

elif mode == "tight":
  x = maxval
  maxa = x // n
  a = [random.randint(1, maxa) for _ in range(n)]

elif mode == "random":
  maxa = maxval
  x = random.randint(1, maxa)
  a = [random.randint(1, maxa) for _ in range(n)]

case = add_case(n, x, a)

print(case)
