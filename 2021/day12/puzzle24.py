from collections import defaultdict

file_ind = 3
file = ["sample12a.txt", "sample12b.txt", "sample12c.txt", "input12.txt"][file_ind]
paths = defaultdict(set)
with open(file, "r") as f:
    for line in f:
        a, b = line.strip().split("-")
        # Make sure we only enter 'start' once
        if a == "start" or b == "end":
            paths[a].add(b)
        elif b == "start" or a == "end":
            paths[b].add(a)
        else:
            paths[a].add(b)
            paths[b].add(a)

print(paths["start"], paths["end"])

full_paths = []


def explore(node, path, used, special_node=None, special_used=False):
    if node == "end":
        path.append("end")
        full_paths.append(list(path))
        path.pop()
        return
    if node.islower():
        if node in used:
            if special_node != node:
                return
            else:
                if special_used:
                    return
                special_used = True
        else:
            used.add(node)
    path.append(node)
    cands = paths[node]
    for c in cands:
        if c in used:
            if special_node is None:
                explore(c, path, used, c, False)
            else:
                continue
        else:
            explore(c, path, used, special_node, special_used)

    path.pop()
    if node.islower():
        if node == special_node:
            return
        else:
            used.remove(node)


used = set()
path = []

explore("start", path, used)
if file_ind < 3:
    for p in full_paths:
        print(p)
ans = len(full_paths)
print(ans)
if file_ind == 0:
    assert ans == 36
elif file_ind == 1:
    assert ans == 103
elif file_ind == 2:
    assert ans == 3509
print("number of paths for {}: {}".format(file, ans))
