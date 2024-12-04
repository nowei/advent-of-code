from collections import Counter

sample = False
file = "sample14.txt" if sample else "input14.txt"
rules = {}
with open(file, "r") as f:
    start = f.readline().strip()
    f.readline()
    for line in f:
        a, b = line.strip().split(" -> ")
        rules[a] = b

poly = start
m = Counter()
for i in range(len(poly) - 1):
    m[poly[i : i + 2]] += 1
for round in range(40):
    temp = Counter()
    for p in m:
        temp[p[0] + rules[p]] += m[p]
        temp[rules[p] + p[1]] += m[p]
    m = temp

counter = Counter()

for p in m:
    for c in p:
        counter[c] += m[p] // 2

# Must account for first and last step being counted only
# once while every other letter gets counted twice.
counter[start[0]] += 1
counter[start[-1]] += 1
mc = counter.most_common()
ans = mc[0][1] - mc[-1][1]

print(ans)
if sample:
    assert ans == 2188189693529
