from typing import Optional, List, Dict, Tuple
import argparse
import bisect

sample_file_path = "test/05.sample"
input_file_path = "test/05.input"
expected_out_part1 = 35
expected_out_part2 = 46

# Function that returns the amount of overlap
def check_overlap(curr, other) -> Optional[Tuple[int, int]]:
    other_start, other_end = other
    start, end = curr
    # c1:
    #  | curr |
    #     | other |
    # c2:
    #     | curr |
    # | other |
    if start <= other_start <= end or other_start <= start <= other_end:
        return (max(start, other_start), min(end, other_end))
    return None

class Conversion_05:
    from_type: str
    to_type: str
    ranges: List[Tuple[int, int, int]]
    converted_ranges: Dict[Tuple[int, int], int]

    def __init__(self, from_type: str, to_type: str, ranges: List[Tuple[int, int, int]]) -> None:
        self.from_type = from_type
        self.to_type = to_type
        self.ranges = ranges
        self.converted_ranges = []
        for r in self.ranges:
            source, destination, range_length = r
            self.converted_ranges.append((source, source + range_length - 1, destination - source))
        self.converted_ranges.sort()

    def convert(self, number: int):
        # Right binary search so that the index can be the number
        # We use filler numbers for the converted range and range length so it only pays attention
        # to the first number.
        insert_index = bisect.bisect_left(self.ranges, (number, float('inf'), float('inf')))
        # return number as the index because there is no converted range
        if insert_index < 0:
            return number
        insert_index -= 1
        source, destination, range_length = self.ranges[insert_index]
        from_range_end = source + range_length
        ret = number
        if number >= source and from_range_end > number:
            diff = number - source
            ret = destination + diff
        return ret
    
    def convert_ranges(self, other_ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        other_ranges.sort()
        res = []
        for a, b in other_ranges:
            overlaps = []
            for c, d, shift in self.converted_ranges:
                overlap = check_overlap((a, b), (c,d))
                if overlap:
                    e, f = overlap
                    overlaps.append((e, f, shift))
            # handle overlaps and shifts
            prev_end = a
            for c, d, shift in overlaps:
                # overlap starts right away
                if prev_end != c:
                    res.append((prev_end, c - 1))
                res.append((c + shift, d + shift))
                prev_end = d
            if not overlaps:
                res.append((a, b))
                prev_end = b
            if prev_end != b:
                res.append((prev_end + 1, b))
        return res


    def __repr__(self):
        inside = "from={},to={},ranges={}".format(self.from_type, self.to_type, self.ranges)
        return "Conversion({})".format(inside)

    def __str__(self):
        return "member of Conversion"

class Almanac_05:
    seed_list: List[int]
    seed_ranges: List[Tuple[int, int]]
    conversion_dict: Dict[str, Conversion_05]

    def __init__(self, seed_list: List[int], conversion_dict: Dict[str, Conversion_05]) -> None:
        self.seed_list = seed_list
        self.seed_ranges = []
        for i in range(0, len(seed_list), 2):
            self.seed_ranges.append((seed_list[i], seed_list[i] + seed_list[i+1] - 1))
        self.conversion_dict = conversion_dict



def parse_file_day05(file_path) -> Almanac_05:
    conversion_dict = {}
    with open(file_path, "r") as f:
        seeds = f.readline()
        seed_list = [int(v) for v in seeds.split(":")[1].strip().split()]
        ranges = []
        from_type = ""
        to_type = ""
        for line in f.readlines():
            stripped = line.strip()
            if stripped == "":
                if len(ranges) > 0:
                    ranges.sort()
                    conversion_dict[from_type] = Conversion_05(from_type, to_type, ranges)
                # Start new object tracking
                ranges = []
            elif "map" in stripped:
                from_type, _, to_type = stripped.split()[0].split("-")
            else:
                destination, source, range_length = [int(v) for v in stripped.split()]
                # Note that we flip the source and destination so we can binary-search
                # easier later on.
                ranges.append(tuple([source, destination, range_length]))
        if len(ranges) > 0:
            ranges.sort()
            conversion_dict[from_type] = Conversion_05(from_type, to_type, ranges)
    return Almanac_05(seed_list, conversion_dict)

def solve_day05_part1(input: Almanac_05) -> int:
    curr = input.seed_list
    convert_type = "seed"
    while convert_type in input.conversion_dict:
        conversion = input.conversion_dict[convert_type]
        curr = [conversion.convert(num) for num in curr]
        convert_type = conversion.to_type
    return min(curr)

def solve_day05_part2(input: Almanac_05) -> int:
    curr = input.seed_ranges
    convert_type = "seed"
    while convert_type in input.conversion_dict:
        conversion = input.conversion_dict[convert_type]
        curr = conversion.convert_ranges(curr)
        convert_type = conversion.to_type
    return min(curr)[0]

def solve_day05(file_path: str, check_out: bool):
    input = parse_file_day05(file_path)
    out_part1 = solve_day05_part1(input)

    if check_out:
        if out_part1 != expected_out_part1:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_out_part1)
        else:
            print("Sample matched")
    print("Part 1 result:")
    print(out_part1)
    print()

    out_part2 = solve_day05_part2(input)
    if check_out:
        if out_part2 != expected_out_part2:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_out_part2)
        else:
            print("Sample matched")
    print("Part 2 result:")
    print(out_part2)
    print()

def main_05(run_all: bool = False):
    print("Running script for day 05")
    print("Sample input")
    solve_day05(sample_file_path, check_out=True)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day05(input_file_path, check_out=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_05(run_all=args.actual)
