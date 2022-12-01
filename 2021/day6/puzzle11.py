sample = False
file = 'sample6.txt' if sample else 'input6.txt'
with open(file, 'r') as f:
    arr = [int(v) for v in f.readline().split(',')]

for i in range(80):
    temp = []
    for v in arr:
        v -= 1
        if v == -1:
            temp.append(6)
            temp.append(8)
        else:
            temp.append(v)
    arr = temp
print('number of fish {}'.format(len(arr)))