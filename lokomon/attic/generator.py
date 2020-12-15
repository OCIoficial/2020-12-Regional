import random
import sys

n = int(sys.argv[2])
permutationness = float(sys.argv[3])

random.seed(sys.argv[1])

mountains = [0 for i in range(n)]

i = 0
j = n - 1

for k in range(n):
    if random.random() < 0.5:
        mountains[i] = k
        i += 1
    else:
        mountains[j] = k
        j -= 1

for i in range(int(permutationness * n)):
    a = random.randint(0, n - 1)
    b = random.randint(0, n - 1)
    mountains[a], mountains[b] = mountains[b], mountains[a]

positions = [0 for i in range(n)]
for i in range(n):
    positions[mountains[i]] = i

print(n)
print(' '.join(map(str, positions)))
