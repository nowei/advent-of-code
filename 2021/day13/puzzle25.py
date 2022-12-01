sample = False
file = "sample13.txt" if sample else "input13.txt"
instruction_flag = False
positions = set()
instructions = []
with open(file, "r") as f:
    for line in f:
        if line.strip() == "":
            instruction_flag = True
        if instruction_flag:
            if not line.strip(): continue
            d, offset = line.strip().split()[2].split('=')
            instructions.append((d, int(offset)))
        else:
            x, y = line.strip().split(',')
            positions.add((int(x), int(y)))

d, offset = instructions[0]
move_cands = set()
stay_cands = set()
for x, y in positions:
    if d == 'x':
        if x > offset:
            move_cands.add((x, y))
        else:
            stay_cands.add((x, y))
    else: # d == 'y'
        if y > offset:
            move_cands.add((x, y))
        else:
            stay_cands.add((x, y))
print(move_cands, stay_cands)
if d == 'x':
    for x, y in move_cands:
        diff = x - offset
        stay_cands.add((offset - diff, y))
else:
    for x, y in move_cands:
        diff = y - offset
        stay_cands.add((x, offset - diff))

positions = stay_cands

ans = len(stay_cands)
print(ans)

if sample:
    assert(ans == 17)