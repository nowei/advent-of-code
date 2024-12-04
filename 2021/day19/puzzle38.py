sample = False
file = "sample19.txt" if sample else "input19.txt"
beacons = {}
with open(file, "r") as f:
    f.readline()
    i = 0
    beacons[0] = set()
    for line in f:
        stripped = line.strip()
        if not stripped:
            i += 1
            beacons[i] = set()
            f.readline()
        else:
            beacons[i].add(tuple(int(c) for c in stripped.split(",")))
num_scanners = i + 1

# Find overlapping beacons
# Will have same offset for 12 beacons
# To find same offset, find pairs of beacons between known beacons of scanners
# If count of beacons is 12, there is overlap.
# If there is overlap, then we can find relative positions of beacons
# We can then merge the information
# If rotated along z direction, there would be a negative rotation of x,y
# If rotated along x direction, there would be a negative rotation of z,y
# If rotated along y direction, there would be a negative rotation of x,z
# e.g. could share same x, but be rotated around
# Need to consider positive and negative versions, along with axes swaps.
from collections import Counter


def scan_beacons(known, candidate):
    # difference map
    # try all combinations and look for 12 with the same differences
    for d in [
        (-1, -1, -1),
        (1, -1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
        (1, 1, -1),
        (1, -1, 1),
        (-1, 1, 1),
        (1, 1, 1),
    ]:
        for o in [(0, 1, 2), (1, 0, 2), (2, 1, 0), (0, 2, 1), (2, 0, 1), (1, 2, 0)]:
            cand = [(d[0] * x[o[0]], d[1] * x[o[1]], d[2] * x[o[2]]) for x in candidate]
            difference_map = Counter()
            for ca, cb, cc in cand:
                for ka, kb, kc in known:
                    # Note that beacons are in unique locations.
                    # This means that the difference will not be the same unless
                    # there is translational symmetry/some overlap.
                    t = (ka - ca, kb - cb, kc - cc)
                    difference_map[t] += 1
                    if difference_map[t] == 12:
                        offset = t
                        best_cand = cand
                        return True, offset, best_cand
    return False, None, None


# Add the offsets to get the things in the original coordinate space
def offset_comp(offset, beacons):
    a, b, c = offset
    adjusted_beacons = set()
    for beacon in beacons:
        ab_x = beacon[0] + a
        ab_y = beacon[1] + b
        ab_z = beacon[2] + c
        ax = [ab_x, ab_y, ab_z]
        adjusted_beacons.add(((ab_x, ab_y, ab_z), beacon))
    return set(a[0] for a in adjusted_beacons)


def print_beacons(beacons):
    s = "({},{},{})," * len(beacons)
    b = []
    for x, y, z in beacons:
        b.append(x)
        b.append(y)
        b.append(z)
    print(s.format(*b))


known_scanners = {0: (0, 0, 0)}
known_beacons = beacons[0]
unknown_scanners = set([i for i in range(1, len(beacons))])
while len(known_scanners) != num_scanners:
    for s in unknown_scanners:
        # Basically try all orientations of this set of beacons and check to see if 12 match
        valid, offset, cand = scan_beacons(known_beacons, beacons[s])
        if valid:
            # add all of the things to the known beacons
            adjusted_beacons = offset_comp(offset, cand)
            known_beacons |= adjusted_beacons
            unknown_scanners.remove(s)
            known_scanners[s] = offset
            break

best_manhattan = 0
for i in range(num_scanners - 1):
    for j in range(i + 1, num_scanners):
        a, b, c = known_scanners[i]
        d, e, f = known_scanners[j]
        man = abs(a - d) + abs(b - e) + abs(c - f)
        if man > best_manhattan:
            best_manhattan = man

ans = best_manhattan
print(ans)
if sample:
    assert ans == 3621
