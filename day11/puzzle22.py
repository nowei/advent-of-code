sample = False
file = "sample11.txt" if sample else "input11.txt"
board = []
with open(file, "r") as f:
    for line in f:
        board.append([int(c) for c in line.strip()])

ans = 0
round = 1
while True:
    flashed = set()
    for i in range(10):
        for j in range(10):
            board[i][j] += 1
            if board[i][j] == 10:
                flashed.add((i, j))
    cand_set = set(flashed)
    while cand_set:
        temp_set = set()
        for i, j in cand_set:
            for k in range(max(i - 1, 0), min(i + 2, 10)):
                for l in range(max(j - 1, 0), min(j + 2, 10)):
                    board[k][l] += 1
                    if board[k][l] == 10:
                        temp_set.add((k, l))
        flashed |= temp_set
        cand_set = temp_set
    if len(flashed) == 100:
        ans = round
        break
    for i, j in flashed:
        board[i][j] = 0
    round += 1
if sample:
    print(ans)
    assert(ans == 195)
    print('sample passed')
else:
    print(ans)