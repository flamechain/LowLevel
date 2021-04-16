import random
import math

samplesize = 100000000

def rand() -> float:
    return random.random()

points = []

for i in range(samplesize):
    points.append([rand(), rand()])

in_circle = 0

for i in points:
    if math.sqrt(i[0]**2 + i[1]**2) < 1:
        in_circle += 1

pi = 4 * (in_circle / samplesize)
print(pi)
