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
for _ in range(10):
    temp = []
    for i in range(len(poly) - 1):
        temp.append(rules[poly[i : i + 2]])
    cand = ""
    for i in range(len(poly) + len(temp)):
        if i % 2 == 0:
            cand += poly[i // 2]
        else:
            cand += temp[i // 2]
    poly = cand

counter = Counter(poly)
mc = counter.most_common()
ans = mc[0][1] - mc[-1][1]

print(ans)
if sample:
    assert ans == 1588
