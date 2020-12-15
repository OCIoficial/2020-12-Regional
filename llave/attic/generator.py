import random
import sys

random.seed(sys.argv[1])

N = int(sys.argv[3])
M = int(sys.argv[4])

if sys.argv[2] == "invalid_too_high":
    A = random.choices(range(1, 10), k=N)
    B = A.copy()
    for i in random.sample(range(N), random.randint(1, min(N, 10))):
        B[i] = random.randint(A[i] + 1, 10)

elif sys.argv[2] == "invalid_more_than_m":
    A = random.choices(range(2, 11), k=N)
    B = A.copy()
    for i in random.sample(range(N), random.randint(M + 1, N)):
        B[i] = random.randint(1, A[i] - 1)

elif sys.argv[2] == "valid_random":
    A = random.choices(range(2, 11), k=N)
    B = A.copy()
    for i in random.sample(range(N), random.randint(0, min(N, M))):
        B[i] = random.randint(1, A[i] - 1)

elif sys.argv[2] == "valid_identical":
    A = random.choices(range(1, 11), k=N)
    B = A.copy()

else:
    sys.exit(42)

print(N, M)
print(" ".join(str(x) for x in A))
print(" ".join(str(x) for x in B))
