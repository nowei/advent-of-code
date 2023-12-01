from collections import Counter 
sample = False
file = 'sample6.txt' if sample else 'input6.txt'
mapping = Counter()
with open(file, 'r') as f:
    for v in f.readline().split(','):
        mapping[int(v)] += 1

for i in range(256):
    temp = Counter()
    for v in mapping:
        v -= 1
        if v == -1:
            temp[6] += mapping[v + 1]
            temp[8] += mapping[v + 1]
        else:
            temp[v] += mapping[v + 1]
    mapping = temp
print('number of fish {}'.format(sum([mapping[v] for v in mapping])))