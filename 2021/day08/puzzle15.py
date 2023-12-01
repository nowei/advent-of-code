sample = False
file = 'sample8.txt' if sample else 'input8.txt'
total = 0
with open(file, 'r') as f:
    for line in f:
        left, right = line.strip().split(' | ')
        level = sum([1 if len(v) in [2, 3, 4, 7] else 0 for v in right.split(' ')])
        total += level
print('total number of 1, 4, 7, and 8s: {}'.format(total))
