from collections import defaultdict

# Process the lines
with open("input4.txt", "r") as f:
    lines = f.readlines()
inputs = [int(i) for i in lines[0].strip().split(",")]
boards = []
for line in lines[1:]:
    if not line.strip():
        boards.append([])
    else:
        boards[-1].append([int(i) for i in line.strip().split()])
board_map = {i: boards[i] for i in range(len(boards))}

# Track board state
count_map = defaultdict(list)
tracker = {}
for ind in range(len(boards)):
    board = boards[ind]
    board_loc = {}
    row_counts = [0 for _ in range(5)]
    col_counts = [0 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            val = board[i][j]
            count_map[val].append(ind)
            board_loc[val] = (i, j)
    tracker[ind] = [board_loc, row_counts, col_counts]

# Find last winner
chosen_val = -1
chosen_ind = -1
seen = set()
cands = {i for i in range(len(boards))}
for val in inputs:
    seen.add(val)
    for ind in count_map[val]:
        if ind not in cands:
            continue
        i, j = tracker[ind][0][val]
        row_counts, col_counts = tracker[ind][1], tracker[ind][2]
        row_counts[i] += 1
        col_counts[j] += 1
        if row_counts[i] == 5 or col_counts[j] == 5:
            cands.remove(ind)
            chosen_ind = ind
            chosen_val = val
            # Break if we are the last winner
            if len(cands) == 0:
                break
    if len(cands) == 0:
        break

print("chosen board ind = {}, chosen val = {}".format(chosen_ind, chosen_val))

chosen_board = board_map[chosen_ind]
print(seen, len(seen), len(inputs))
for line in chosen_board:
    print(line)
total_unused = sum(
    [sum([v for v in row if v not in seen] + [0]) for row in chosen_board]
)
print("final score: {}".format(total_unused * chosen_val))
