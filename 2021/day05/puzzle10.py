from collections import Counter
sample = False
file = 'sample5.txt' if sample else 'input5.txt' 
vents = []
with open(file, 'r') as f:
    for line in f:
        a, b = line.strip().split(' -> ')
        x1, y1 = a.split(',')
        x2, y2 = b.split(',')
        arr = [int(v) for v in [x1, y1, x2, y2]]
        vents.append(arr)

counts = Counter()
for x1, y1, x2, y2 in vents:
    if x1 == x2:
        x = x1
        for y in range(min(y1, y2), max(y1, y2) + 1):
            counts[(x, y)] += 1
    elif y1 == y2:
        y = y1
        for x in range(min(x1, x2), max(x1, x2) + 1):
            counts[(x, y)] += 1
    else:
        if x2 > x1 and y2 > y1: # top left to bot right
            x = True
            y = True
        elif x2 > x1 and y2 < y1: # top right to bot left
            x = True
            y = False
        elif x2 < x1 and y2 > y1: # bot left to top right
            x = False
            y = True
        else: # x2 < x1 and y2 < y1 # bot right to top left
            x = False
            y = False
        for i in range(abs(x2 - x1) + 1):
            counts[(x1 + (i if x else -i), y1 + (i if y else -i))] += 1
total = 0
for c in counts:
    if counts[c] > 1:
        total += 1
print('number of at least two overlap is: {}'.format(total))
