from collections import deque

sample = True
file = "sample23.txt" if sample else "input23.txt"
with open(file, "r") as f:
    f.readline()
    hallway_length = len(f.readline().strip().strip('#'))        
    level1 = f.readline().strip().strip('###').split('#')
    level2 = f.readline().strip().split('#')[1:]
    rooms = [[level1[i], level2[i]] for i in range(len(level1))]
print(rooms, hallway_length)
# BFS until move a piece, then if we moved, know that it was an okay move 
hallway = '.' * hallway_length
state = (hallway, rooms)
print(state)

def get_valid_moves(state, history, cost = 0, turn=0):
    hallway, rooms = state
    moves_to_consider = []

    for i, v in enumerate(hallway):
        if v != '.':
            moves_to_consider.extend(get_moves(state, i, cost, False, turn, history))
    if rooms[0] and not all([p == 'A' for p in rooms[0]]):
        moves_to_consider.extend(get_moves(state, 0, cost, True, turn, history))
    if rooms[1] and not all([p == 'B' for p in rooms[1]]):
        moves_to_consider.extend(get_moves(state, 1, cost, True, turn, history))
    if rooms[2] and not all([p == 'C' for p in rooms[2]]):
        moves_to_consider.extend(get_moves(state, 2, cost, True, turn, history))
    if rooms[3] and not all([p == 'D' for p in rooms[3]]):
        moves_to_consider.extend(get_moves(state, 3, cost, True, turn, history))
    return moves_to_consider

goal_map = {'A':0, 'B':1, 'C':2, 'D':3}
room_hallway_ind = {0: 2, 1: 4, 2: 6, 3: 8}
move_map = {'A':1, 'B':10, 'C':100, 'D':1000}

def get_moves(state, i, cost, room, turn, history):
    hallway, rooms = state
    cand_moves = []
    if room:
        cand = rooms[i][0]
        curr_ind = room_hallway_ind[i]
    else:
        cand = hallway[i]
        curr_ind = i
    move_cost = move_map[cand]
    goal = goal_map[cand]
    j = curr_ind - 1
    for j in range(curr_ind - 1, -1, -1):
        if hallway[j] != '.':
            j += 1
            break
    hallway_ind_min = j
    j = curr_ind + 1
    for j in range(curr_ind + 1, len(hallway)):
        if hallway[j] != '.':
            j -= 1
            break
    hallway_ind_max = j
    goal_ind = room_hallway_ind[goal]
    nothing_between = hallway_ind_min <= goal_ind <= hallway_ind_max

    if room:
        get_out_moves = 2 if len(rooms[i]) == 1 else 1
        # Can't move outside of any room 
        if (len(rooms[goal]) == 0 or (len(rooms[goal]) == 1 and rooms[goal][0] == cand)) and nothing_between:
            get_in_moves = 1 if len(rooms[goal]) == 1 else 2
            moves = get_out_moves + get_in_moves + abs(curr_ind - goal_ind)
            new_rooms = [list(l) for l in rooms]
            new_rooms[i].pop(0)
            new_rooms[goal].insert(0, cand)
            new_state = (hallway, new_rooms)
            cand_moves.append([cost + moves * move_cost, new_state, True, turn, history + [new_state]])
        else:
            valid_rests = [p for p in [0, 1, 3, 5, 7, 9, 10] if hallway_ind_min <= p <= hallway_ind_max]
            valid_rests.sort(key=lambda x: abs(x - goal_ind))
            for rest in valid_rests:
                moves = abs(curr_ind - rest) + get_out_moves
                new_rooms = [list(l) for l in rooms]
                new_rooms[i].pop(0)
                new_hallway = hallway[:rest] + cand + hallway[rest + 1:]
                new_state = (new_hallway, new_rooms)
                cand_moves.append([cost + moves * move_cost + turn_cost, new_state, False, turn + 1, history + [new_state]])
    else:
        if (len(rooms[goal]) == 0 or (len(rooms[goal]) == 1 and rooms[goal][0] == cand)) and nothing_between:
            get_in_moves = 1 if len(rooms[goal]) == 1 else 2
            moves = get_in_moves + abs(curr_ind - goal_ind)
            new_rooms = [list(l) for l in rooms]
            new_rooms[goal].insert(0, cand)
            new_hallway = hallway[:curr_ind] + '.' + hallway[curr_ind + 1:]
            new_state = (new_hallway, new_rooms)
            cand_moves.append([cost + moves * move_cost, new_state, True, turn, history + [new_state]])
    return cand_moves

def validate_end(state):
    hallway, rooms = state
    conds = []
    conds.append(len(rooms[0]) == 2 and all([p == 'A' for p in rooms[0]]))
    conds.append(len(rooms[1]) == 2 and all([p == 'B' for p in rooms[1]]))
    conds.append(len(rooms[2]) == 2 and all([p == 'C' for p in rooms[2]]))
    conds.append(len(rooms[3]) == 2 and all([p == 'D' for p in rooms[3]]))
    return all(conds)

import heapq

turn_cost = 1000
cost = 0
moves = get_valid_moves(state, [state])
heapq.heapify(moves)
while moves:
    c, s, plopped, turn, history = heapq.heappop(moves)
    print('considering w/ cost {} turn {} {}                '.format(c, turn, s), end='\r')
    if plopped:
        # cost += c
        # print()
        # print('next moves starting from')
        # print(s)
        # moves = get_valid_moves(s)
        next_moves = get_valid_moves(s, history, c, turn)
        if not next_moves and validate_end(s): 
            break
        for m in next_moves:
            heapq.heappush(moves, m)
    else:
        next_moves = get_valid_moves(s, history, c, turn)
        for m in next_moves:
            heapq.heappush(moves, m)
print()
print(c)
ans = c - turn * turn_cost
for h in history:
    print(h)
print(ans)
if sample:
    assert(ans == 12521)