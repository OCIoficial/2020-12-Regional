import random
import sys

n = int(sys.argv[2])

random.seed(str(sys.argv))
mountains = random.sample(range(n), k=n)

print(n)
print(' '.join(map(str, list(mountains))))
