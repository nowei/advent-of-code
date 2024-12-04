import heapq

sample = False
file = "sample15.txt" if sample else "input15.txt"
grid = []
with open(file, "r") as f:
    for line in f:
        grid.append([])
        for pos in line.strip():
            grid[-1].append(int(pos))

n = len(grid)
m = len(grid[0])

q = [(0, 0, 0)]
seen = set()
costs = {}
while q and (n - 1, m - 1) not in seen:
    c, x, y = heapq.heappop(q)
    if (x, y) in seen:
        continue
    costs[(x, y)] = c
    seen.add((x, y))
    if x > 0 and (x - 1, y) not in seen:  # try left
        heapq.heappush(q, (c + grid[x - 1][y], x - 1, y))
    if x < n - 1 and (x + 1, y) not in seen:  # try right
        heapq.heappush(q, (c + grid[x + 1][y], x + 1, y))

    if y > 0 and (x, y - 1) not in seen:  # try up
        heapq.heappush(q, (c + grid[x][y - 1], x, y - 1))

    if y < m - 1 and (x, y + 1) not in seen:  # try down
        heapq.heappush(q, (c + grid[x][y + 1], x, y + 1))

ans = costs[(n - 1, m - 1)]
print(ans)
if sample:
    assert ans == 40
