mapping = [{"0":0, "1":0} for _ in range(12)]
cands = []
with open('input5.txt', 'r') as f:
    for line in f:
        cands.append(line.strip())
def find_oxygen_generator_rating(cands, co2_scrubber=False):
    ind = 0
    while len(cands) > 1:
        zeros = 0
        ones = 0
        for c in cands:
            if c[ind] == "0":
                zeros += 1
            else:
                ones += 1
        if co2_scrubber:
            cond = ones < zeros
        else:
            cond = ones >= zeros
        if cond:
            cands = [c for c in cands if c[ind] == "1"]
        else:
            cands = [c for c in cands if c[ind] == "0"]
        ind += 1
    return int(cands[0], 2)

o2 = find_oxygen_generator_rating(cands)
co2 = find_oxygen_generator_rating(cands, co2_scrubber=True)
print('o2 = {}, co2 = {}'.format(o2, co2))
print('life support rating = {}'.format(o2 * co2))
