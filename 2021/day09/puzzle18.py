sample = True
file = "sample9.txt" if sample else "input9.txt"
area = []
with open(file, "r") as f:
    for line in f:
        area.append([int(v) for v in line.strip()])


def explore(seen, i, j):
    if (i, j) in visited or (i, j) in seen:
        return
    if i < 0 or i >= len(area) or j < 0 or j >= len(area[0]) or area[i][j] == 9:
        return
    seen.add((i, j))
    explore(seen, i + 1, j)
    explore(seen, i - 1, j)
    explore(seen, i, j - 1)
    explore(seen, i, j + 1)


basins = []
visited = set()
for i in range(len(area)):
    for j in range(len(area[0])):
        if area[i][j] != 9 and (i, j) not in visited:
            seen = set()
            explore(seen, i, j)
            basins.append(seen)
            visited |= seen

basins = sorted(basins, key=lambda x: -len(x))
good_basins = basins[:3]
basin_lens = [len(b) for b in good_basins]

print(basin_lens[0] * basin_lens[1] * basin_lens[2])
