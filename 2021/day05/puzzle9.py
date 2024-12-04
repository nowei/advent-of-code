from collections import Counter

sample = False
file = "sample5.txt" if sample else "input5.txt"
vents = []
with open(file, "r") as f:
    for line in f:
        a, b = line.strip().split(" -> ")
        x1, y1 = a.split(",")
        x2, y2 = b.split(",")
        arr = [int(v) for v in [x1, y1, x2, y2]]
        if arr[0] == arr[2] or arr[1] == arr[3]:
            vents.append(arr)

counts = Counter()
for x1, y1, x2, y2 in vents:
    if x1 == x2:
        x = x1
        for y in range(min(y1, y2), max(y1, y2) + 1):
            counts[(x, y)] += 1
    else:  # y1 == y2
        y = y1
        for x in range(min(x1, x2), max(x1, x2) + 1):
            counts[(x, y)] += 1
total = 0
for c in counts:
    if counts[c] > 1:
        total += 1
print("number of at least two overlap is: {}".format(total))
