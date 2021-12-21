from collections import defaultdict, Counter 

sample = False
file = "sample21.txt" if sample else "input21.txt"
positions = {}
with open(file, "r") as f:
    positions[0] = int(f.readline().strip().split()[-1]) - 1
    positions[1] = int(f.readline().strip().split()[-1]) - 1
print(positions)

# 3 * 3 * 3 possible outcomes
# On each turn, 27 possible outcomes for dice rolls
# There are 7 such unique outcomes with distribution
# 3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1
# Then count of pos + outcome becomes product of num at pos and num of outcome
# each score then needs to keep track of the number of ways to get to that score from that position
# Any score greater than or equal to 21 gets added to universe wins
outcomes = Counter()
for i in range(1,4):
    for j in range(1,4):
        for k in range(1, 4):
            outcomes[i+j+k] += 1
print(outcomes)


# If both start at 1, 1
# possible outcomes after p1 is
# (4,0; 4,1):1, (5,0; 5,1):3, (6,0; 6,1):6, (7,0; 7,1):7, (8,0; 8,1):6, (9,0; 9,1):4, (10,0; 10,1):1
# possible outcomes at the end of turn 2 for p2 is
#  (4,4;  4,4): 1,  (4,5; 4,5):  3,  (4,6; 4,6):  6,  (4,7: 4,7):  7,   (4,8; 4,8): 6,   (4,9; 4,9): 3,   (4,10; 4,10): 1
#  (5,4;  5,4): 3,  (5,5; 5,5):  9,  (5,6; 5,6): 18,  (5,7: 5,7): 21,  (5,8; 5,8): 18,   (5,9; 5,9): 9,   (5,10; 5,10): 3
#  (6,4;  6,4): 6,  (6,5; 6,5): 18,  (6,6; 6,6): 36,  (6,7: 6,7): 42,  (6,8; 6,8): 36,  (6,9; 6,9): 18,   (6,10; 6,10): 6
#  (7,4;  7,4): 7,  (7,5; 7,5): 21,  (7,6; 7,6): 42,  (7,7: 7,7): 49,  (7,8; 7,8): 42,  (7,9; 7,9): 21,   (7,10; 7,10): 7
#  (8,4;  8,4): 6,  (8,5; 8,5): 18,  (8,6; 8,6): 36,  (8,7: 8,7): 42,  (8,8; 8,8): 36,  (8,9; 8,9): 18,   (8,10; 8,10): 6
#  (9,4;  9,4): 3,  (9,5; 9,5):  9,  (9,6; 9,6): 18,  (9,7: 9,7): 21,  (9,8; 9,8): 18,   (9,9; 9,9): 9,   (9,10; 9,10): 3
# (10,4; 10,4): 1, (10,5; 10,5): 3, (10,6; 10,6): 6, (10,7: 10,7): 7, (10,8; 10,8): 6, (10,9; 10,9): 4, (10,10; 10,10): 1
# Then for each of these outcomes, 

# state[(s1, s2, p1, p2)] = count
# score: 21 * 21, position: 10 * 10 = 441 * 100 <= 44100 comps per iteration
# universe_wins = [0, 0]
# 

# to get to 21 from pos 1,
# 9 -> 10 lands on 10
# 9 -> 10 + 9 = 19 lands on 9
# 3 -> 10 + 9 + 2 = 21 lands on 2
# min number of turns is 3 for a player to get results

# minimum path to 21 from 1 is 9 moves
# rolling 3 -> 4,4 ; 
#         9 -> 7,3 ; 
#         9 -> 9,2 ; 
#         9 -> 10,1; 
#         3 -> 14,4; 
#         9 -> 17,3; 
#         9 -> 19,2; 
#         9 -> 20,1; 
#         # -> 21,#
# so paths should end in at most 17 turns 

turn = 0
t = 0
won_universes = [0, 0]
state = {(0, 0, positions[0], positions[1]):1}
# state = {(0, 0, 0, 0):1}
print('starting state', state)
for _ in range(17):
    new_state = Counter()
    for s in state:
        s1, s2, p1, p2 = s
        if turn:
            pos = p2
        else:
            pos = p1
        for outcome in outcomes:
            new_pos = pos + outcome
            new_pos %= 10
            if turn:
                new_score = s2 + new_pos + 1
            else: 
                new_score = s1 + new_pos + 1
            # if new_score == 1:
            #     print('wtffff', new_pos, pos, outcome)
            num_universes = state[s] * outcomes[outcome]
            if turn:
                ns = (s1, new_score, p1, new_pos)
            else:
                ns = (new_score, s2, new_pos, p2)
            if new_score >= 21:
                won_universes[turn] += num_universes
            else:
                # Note: We need to add num_universes because there's multiple ways
                # to reach the same state from a previous state. 
                # e.g. (9, 9) can be reached from (9, 4), (9, 5), (9, 6), (9, 7), (9, 8)
                new_state[ns] += num_universes
    print(t, turn, won_universes)
    state = new_state
    turn ^= 1
    t += 1


print(won_universes)
ans = max(won_universes)
print(ans)
if sample:
    assert(ans == 444356092776315)
    assert(min(won_universes) == 341960390180808)