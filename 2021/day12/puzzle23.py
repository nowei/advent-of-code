from collections import defaultdict
file_ind = 3
file = ['sample12a.txt','sample12b.txt','sample12c.txt','input12.txt'][file_ind]
paths = defaultdict(set)
with open(file, "r") as f:
    for line in f:
        a, b = line.strip().split('-')
        paths[a].add(b)
        paths[b].add(a)

full_paths = []
def explore(node, path, used):
    if node == 'end':
        path.append('end')
        full_paths.append(list(path))
        return
    if node.islower():
        if node in used: 
            return
        else: 
            used.add(node)
    path.append(node)
    cands = paths[node]
    for c in cands:
        explore(c, path, used)
    path.pop()
    if node.islower():
        used.remove(node)

used = set()
path = []

explore('start', path, used)
if file_ind < 3:
    for p in full_paths:
        print(p)
ans = len(full_paths)
if file_ind == 0:
    assert(ans == 10)
elif file_ind == 1:
    assert(ans == 19)
elif file_ind == 2: 
    assert(ans == 226)
print('number of paths for {}: {}'.format(file, ans))