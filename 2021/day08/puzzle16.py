sample = False
file = 'sample8.txt' if sample else 'input8.txt'
numbers = []
digits = []
with open(file, 'r') as f:
    for line in f:
        left, right = line.strip().split(' | ')
        numbers.append([''.join(sorted(v)) for v in left.split(' ')])
        digits.append([''.join(sorted(v)) for v in right.split(' ')])
# 0 -> 6
# 1 -> 2
# 2 -> 5
# 3 -> 5
# 4 -> 4
# 5 -> 5
# 6 -> 6
# 7 -> 3
# 8 -> 7
# 9 -> 6

# 2 -> [1]
# 3 -> [7]
# 4 -> [4]
# 5 -> [2, 3, 5]
# 6 -> [0, 6, 9]
# 7 -> [8]
total = 0
for i in range(len(numbers)):
    nums = numbers[i]
    digs = digits[i]
    mapping = {}
    dir_map = {}
    ans_map = {}
    mapping[1] = next(v for v in nums if len(v) == 2)
    mapping[7] = next(v for v in nums if len(v) == 3)
    mapping[4] = next(v for v in nums if len(v) == 4)
    mapping[8] = next(v for v in nums if len(v) == 7)
    unknowns = {5: [v for v in nums if len(v) == 5], 6: [v for v in nums if len(v) == 6]}
    # 3 if right side matches 1
    mapping[3] = next(cand for cand in unknowns[5] if all(m in cand for m in mapping[1]))
    # 6 if not all right side matches 1
    mapping[6] = next(cand for cand in unknowns[6] if not all(m in cand for m in mapping[1]))
    # 2 if 4 lines matches 6 and not 3
    mapping[2] = next(cand for cand in unknowns[5] if cand != mapping[3] and sum([1 if m in cand else 0 for m in mapping[6]]) == 4)
    # 5 is remaining of [2, 3, 5]
    mapping[5] = next(cand for cand in unknowns[5] if cand not in [mapping[2], mapping[3]])
    # 0 if 4 lines matches 5
    mapping[0] = next(cand for cand in unknowns[6] if sum([1 for m in cand if m in mapping[5]]) == 4)
    # 9 if not 0 and not 6
    mapping[9] = next(cand for cand in unknowns[6] if cand not in [mapping[0], mapping[6]])
    for k in mapping:
        ans_map[mapping[k]] = k
    assert(len(ans_map) == 10)
    assert(len(set([ans_map[k] for k in ans_map])) == 10)
    
    curr = 0
    for v in digs:
        curr *= 10
        curr += ans_map[v]
    total += curr
print('total after sum is {}'.format(total))
