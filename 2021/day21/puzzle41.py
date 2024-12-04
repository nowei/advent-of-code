sample = False
file = "sample21.txt" if sample else "input21.txt"
pos = []
with open(file, "r") as f:
    for line in f:
        pos.append(int(line.strip().split()[-1]))
print(pos)
pos[0] -= 1
pos[1] -= 1

dice = 1
turn = 0
rolls = 0
score = [0, 0]
t = 0

while score[0] < 1000 and score[1] < 1000:
    curr = 0
    for i in range(3):
        curr += dice
        dice += 1
        rolls += 1
        if dice == 101:
            dice = 1
    pos[turn] += curr
    pos[turn] %= 10
    score[turn] += pos[turn] + 1
    turn ^= 1
    t += 1
    print(t, turn, curr, pos, score)

print(rolls, score)

ans = rolls * min(score)
print(ans)
if sample:
    assert ans == 739785
