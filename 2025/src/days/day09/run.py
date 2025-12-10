from typing import List, Tuple
from collections import defaultdict

InputType = List[Tuple[int, int]]
parent_path = "src/days/day09/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    out = []
    with open(file_name, "r") as f:
        for line in f:
            out.append(tuple([int(v) for v in line.strip().split(",")]))
    return out


def part1(_input: InputType) -> int:
    best = 0
    for i in range(len(_input) - 1):
        for j in range(i + 1, len(_input)):
            x_i, y_i = _input[i]
            x_j, y_j = _input[j]
            d_x = abs(x_i - x_j) + 1
            d_y = abs(y_i - y_j) + 1
            if d_x * d_y > best:
                best = d_x * d_y
    return best


# original border crossings code
def part2_bad(_input: InputType) -> int:
    max_size = 12
    if _input[0][0] > 100:
        max_size = 100_000
    # generate shape
    total_spaces = []
    # build inclusive ranges
    inclusive_ranges = defaultdict(list)
    for i in range(0, len(_input)):
        x_i, y_i = _input[i - 1]
        x_j, y_j = _input[i]
        if x_i == x_j:
            x = x_i
            for y in range(min(y_i, y_j), max(y_i, y_j) + 1):
                total_spaces.append((x, y))
                inclusive_ranges[y].append((x, x))
        else:
            y = y_i
            for x in range(min(x_i, x_j), max(x_i, x_j) + 1):
                total_spaces.append((x, y))

            inclusive_ranges[y].append((x_i, x_j))

    total_spaces_set = set(total_spaces)
    fill_spaces = set()
    print(total_spaces)

    for y in range(0, max_size):
        x = 0
        while (x, y) not in total_spaces_set and x < max_size:
            x += 1
        while x < max_size:
            # Border crossing
            cands = []
            while (x, y) in total_spaces_set:
                x += 1
            while (x, y) not in total_spaces_set and x < max_size:
                cands.append((x, y))
                x += 1
            if (x, y) in total_spaces_set:
                fill_spaces.update(cands)

    print(len(total_spaces))
    print(len(fill_spaces))
    print(min([x[0] for x in total_spaces]), max([x[0] for x in total_spaces]))
    print(min([y[1] for y in total_spaces]), max([y[1] for y in total_spaces]))
    if max_size < 100:
        for y in range(0, max_size + 1):
            s = ""
            for x in range(0, max_size + 1):
                if (x, y) in fill_spaces:
                    s += "X"
                elif (x, y) in total_spaces_set:
                    s += "#"
                else:
                    s += "."
            print(s)
    return 0


def part2_ranges(_input: InputType) -> int:
    max_size = 12
    if _input[0][0] > 100:
        max_size = 100_000
    # build inclusive ranges
    inclusive_ranges = defaultdict(list)
    for i in range(0, len(_input)):
        x_i, y_i = _input[i - 1]
        x_j, y_j = _input[i]
        if x_i == x_j:
            x = x_i
            for y in range(min(y_i, y_j) + 1, max(y_i, y_j)):
                inclusive_ranges[y].append((x, x))
        else:
            y = y_i
            inclusive_ranges[y].append((min(x_i, x_j), max(x_i, x_j)))
    for y in inclusive_ranges:
        inclusive_ranges[y] = sorted(inclusive_ranges[y])
    # This interprets:
    # .............
    # .......#XXX#..
    # .......X...X..
    # ..#XXXX#...X..
    # ..X........X..
    # ..#XXXXXX#.X..
    # .........X.X..
    # .........#X#..
    # ..............
    # as
    # 1 [(7, 11)]
    # 2 [(7, 7), (11, 11)]
    # 3 [(2, 7), (11, 11)]
    # 4 [(2, 2), (11, 11)]
    # 5 [(2, 9), (11, 11)]
    # 6 [(9, 9), (11, 11)]
    # 7 [(9, 11)]
    inclusive_innards = defaultdict(list)

    # Cases
    # Simple:
    # ...XOOOX...
    # ..XXX..XOOOX...
    # ...XOOXXXOOX...
    # ...XXXOOOXXX...
    previous_level_innards = []
    for y in range(0, max_size + 1):
        current_level_outline = inclusive_ranges[y]
        candidate_innards_init = []
        # Since we have marked the borders, we can do a row-by-row fill
        # for every pair we evaluate, if all the entries between two consecutive
        # ranges were included in the inclusive_ranges + inclusive_innards,
        # we add it to the next level of inclusive innards
        for i in range(len(current_level_outline)):
            candidate_innards_init.append(current_level_outline[i])
        # Between two consecutive ranges, check if the previous level
        # merge ranges
        candidate_innards = []
        if len(candidate_innards_init) == 1:
            candidate_innards = candidate_innards_init
        else:  # actually need to check ranges between these
            for i in range(1, len(candidate_innards_init)):
                x1, x2 = candidate_innards_init[i - 1]
                x3, x4 = candidate_innards_init[i]
                for ranges in previous_level_innards:
                    if ranges[0] <= x2 and x3 <= ranges[1]:
                        candidate_innards.append((x1, x4))
                        break
            # Check each one, if it doesn't have anything above, it is a
            # progenitor range
            for i in range(len(candidate_innards_init)):
                x1, x2 = candidate_innards_init[i]
                if not any(
                    ranges[0] <= x1 and x2 <= ranges[1]
                    for ranges in previous_level_innards
                ):
                    candidate_innards.append((x1, x2))
            # merge ranges
            candidate_innards = sorted(candidate_innards)
            final_cand_innards = []
            if candidate_innards:
                final_cand_innards = [candidate_innards[0]]
            for i in range(1, len(candidate_innards)):
                curr = candidate_innards[i]
                if (
                    final_cand_innards[-1][0] <= curr[0]
                    and curr[0] <= final_cand_innards[-1][1]
                ):
                    final_cand_innards[-1] = (
                        final_cand_innards[-1][0],
                        max(curr[1], final_cand_innards[-1][1]),
                    )
                else:
                    final_cand_innards.append(curr)
            candidate_innards = final_cand_innards
        inclusive_innards[y] = candidate_innards
        previous_level_innards = inclusive_innards[y]
    for y in inclusive_innards:
        inclusive_innards[y] = sorted(inclusive_innards[y])
    # Thus, between every pair of numbers,
    prev = (tuple([(0, 0), (0, 0)]), tuple([(0, 0)]))
    for y in range(0, max_size + 1):
        if y in inclusive_ranges:
            curr = (tuple(inclusive_ranges[y]), tuple(inclusive_innards[y]))
            if curr != prev:
                print(y, inclusive_ranges[y], inclusive_innards[y])
            prev = curr
    # To determine the area inside, we take every two corner points...
    # Note that this is reasonable to compute because there are less than
    # 500 points, so there are at most 250000 comparisons
    # And we can easily rule out things that don't exist within the inclusive_innards
    # We can further skip any points that aren't to the right and below the current point
    # of interest.
    best = 0
    # 254566822 is too low
    # answer was 1574684850 # 245.767s
    sorted_input = sorted(_input)
    for i in range(len(sorted_input) - 1):
        x_i, y_i = sorted_input[i]
        for j in range(i + 1, len(sorted_input)):
            x_j, y_j = sorted_input[j]
            min_x = min(x_i, x_j)
            max_x = max(x_i, x_j)
            min_y = min(y_i, y_j)
            max_y = max(y_i, y_j)
            if (abs(x_i - x_j) + 1) * (
                abs(y_i - y_j) + 1
            ) < best:  # Adding this made it 90s faster (154s)
                continue
            all_satisfies = True
            for y in range(min_y, max_y + 1):
                # A range must fully include x_i to x_j for it to be a valid row
                all_satisfies = any(
                    ranges[0] <= min_x and max_x <= ranges[1]
                    for ranges in inclusive_innards[y]
                )
                if not all_satisfies:
                    break
            if all_satisfies:
                best = max(best, (abs(x_i - x_j) + 1) * (abs(y_i - y_j) + 1))
                print("all satisfied,", i, j, (x_i, y_i), (x_j, y_j), best)
            # all satisfied, 0 1 (1659, 45009) (1659, 46194) 1186
            # all satisfied, 0 4 (1659, 45009) (1766, 46194) 128088
            # all satisfied, 0 478 (1659, 45009) (97858, 45256) 23857600
            # all satisfied, 0 483 (1659, 45009) (97923, 45256) 23873720
            # all satisfied, 1 478 (1659, 46194) (97858, 45256) 90331800
            # all satisfied, 2 438 (1712, 47430) (94985, 48652) 114074102
            # all satisfied, 4 438 (1766, 46194) (94985, 48652) 229227980
            # all satisfied, 10 438 (2134, 43813) (94985, 48652) 449403680
            # all satisfied, 16 474 (2366, 51083) (97692, 56197) 487597605
            # all satisfied, 18 438 (2392, 42665) (94985, 48652) 554452872
            # all satisfied, 20 474 (2456, 50114) (97692, 56197) 579421908
            # all satisfied, 24 438 (2924, 41407) (94985, 48652) 667081252
            # all satisfied, 29 439 (3127, 58277) (94985, 50114) 749936876
            # all satisfied, 32 438 (3480, 39024) (94985, 48652) 881111274
            # all satisfied, 37 439 (3568, 60649) (94985, 50114) 963180048
            # all satisfied, 39 439 (3727, 61854) (94985, 50114) 1071471919
            # all satisfied, 45 439 (3935, 63053) (94985, 50114) 1178199940
            # all satisfied, 48 439 (4158, 64351) (94985, 50114) 1293209064
            # all satisfied, 49 439 (4158, 65538) (94985, 50114) 1401021900
            # all satisfied, 53 439 (4679, 66653) (94985, 50114) 1493677780
            # all satisfied, 57 439 (5388, 67688) (94985, 50114) 1574684850
            # actual result...
            # 1574684850

    return best


def part2(_input: InputType) -> int:  # wtf
    x_coords = sorted(set([x for (x, _y) in _input]))
    y_coords = sorted(set([y for (_x, y) in _input]))
    x_mapping = {}
    y_mapping = {}
    x_reverse_mapping = {}
    y_reverse_mapping = {}
    for i in range(len(x_coords)):
        x_mapping[i] = x_coords[i]
        x_reverse_mapping[x_coords[i]] = i
    for i in range(len(y_coords)):
        y_mapping[i] = y_coords[i]
        y_reverse_mapping[y_coords[i]] = i
    total_spaces = []
    mapped_input = [(x_reverse_mapping[x], y_reverse_mapping[y]) for x, y in _input]
    for i in range(0, len(_input)):
        x_i, y_i = mapped_input[i - 1]
        x_j, y_j = mapped_input[i]

        if x_i == x_j:
            x = x_i
            for y in range(min(y_i, y_j), max(y_i, y_j) + 1):
                total_spaces.append((x, y))
        else:
            y = y_i
            for x in range(min(x_i, x_j), max(x_i, x_j) + 1):
                total_spaces.append((x, y))
    total_spaces_set = set(total_spaces)
    for y in range(0, len(y_coords) + 1):
        s = ""
        for x in range(0, len(x_coords) + 1):
            if (x, y) in total_spaces_set:
                s += "#"
            else:
                s += "."
    # All that remains is figuring out the largest area within the shape and then mapping it back to the original coordinates...
    return 0


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
