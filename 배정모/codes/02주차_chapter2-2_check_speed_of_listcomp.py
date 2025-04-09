import time

N = 1000000

# listcomp 방식
start1 = time.time()
result1 = [x**2 for x in range(N) if x % 2 == 0]
end1 = time.time()
print(f"List comprehension: {end1 - start1:.4f}초")

# map + filter 방식
start2 = time.time()
result2 = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(N))))
end2 = time.time()
print(f"map + filter:      {end2 - start2:.4f}초")

# List comprehension: 0.0993초
# map + filter:      0.1302초


colors = ['black','green','yellow']
sizes = ['S','M','L','XL']
for cloth in (f"{c}_{s}" for c in colors for s in sizes):
    print(cloth)