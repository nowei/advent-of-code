from typing import Any, List, Dict, Tuple
import argparse
import bisect

sample_file_path = "test/05.sample"
input_file_path = "test/05.input"
expected_out_part1 = 35
expected_out_part2 = 46

def check_overlap(curr, collapsed) -> bool:
    if not collapsed:
        return False
    prev_start, prev_end, _ = collapsed[-1]
    start, end, _ = curr
    #  | curr |
    #     | prev |
    if start <= prev_start <= end:
        return True
    #     | curr |
    # | prev |
    if prev_start <= start <= prev_end:
        return True
    return False

class Conversion_05:
    from_type: str
    to_type: str
    ranges: List[Tuple[int, int, int]]
    converted_range: Dict[Tuple[int, int], int]

    def __init__(self, from_type: str, to_type: str, ranges: List[Tuple[int, int, int]]) -> None:
        self.from_type = from_type
        self.to_type = to_type
        self.ranges = ranges
        self.converted_range = []
        for r in self.ranges:
            source, destination, range_length = r
            self.converted_range.append((source, source + range_length - 1, destination - source))
        self.converted_range.sort()

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
    

    # Part 2, the idea is that we can convert ranges by determining the start
    # And end ranges and figuring out how to map between those. 
    # E.g.
    # last conversion index: 
    # (56, 60, 37), (93, 56, 4) -> ([56-92] -> [60-96]), ([93-96] -> [56-59])
    # second to last conversion index:
    # (0, 1, 69), (69, 0, 1) -> ([0-68] -> [1-69]), ([69-69] -> [0-0])
    # resulting inverted examples are
    # [[0, 68], 1]
    # [[69, 69], -69]
    # then
    # [[56, 92], 4]
    # [[93, 96], -37]
    # Then we want to combine these
    # so we have 
    # [[0, 55], 1]
    # [[56, 68], 5]
    # [[69, 69], -65]
    # [[70, 92], 4]
    # [[93, 96], -37]
    # [[97,100], 0]
    # Note that ranges are inclusive
    def invert(self, other_ranges: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        # start with other_ranges
        # combine with ranges as we go
        ranges_copy = other_ranges.copy()
        for r in self.converted_range:
            bisect.insort_left(ranges_copy, r)
        # collapse
        print("rp", ranges_copy)
        # Note that these ranges will have at most 2 things starting with the same start index
        # [(0, 68, 1), (56, 92, 4), (69, 69, -69), (93, 96, -37)]
        # [(0, 55, 1), (56, 68, 5), (69, 69, -65), (70, 92, 4), (93, 96, -37)]
        # So special handling only really needs to happen between the current and previous blocks
        collapsed = []
        for curr in ranges_copy:
            start, end, shift = curr
            to_merge = []
            # If there is overlap with the previous thing, handle it.
            # Collapsed items should be non-overlapping here
            while check_overlap(curr, collapsed):
                to_merge.append(collapsed.pop())
            to_merge.reverse()
            while to_merge: 
                prev_start, prev_end, prev_shift = to_merge.pop()
                # (69, 92, 4) + (69, 69, -69) = (69, 69, -65) + (70, 92, 4)
                if prev_start == start:
                    # e.g. [[1, 5, 2]] + [1, 9, 4]
                    # [1, 5, 2] + [1, 9, 4] = [1, 5, 6] + [6, 9, 4]
                    start = min(prev_end, end) + 1
                    first_cut = start - 1
                    curr_shift = prev_shift + shift
                    collapsed.append((prev_start, first_cut, curr_shift))
                    end = max(prev_end, end)
                    shift = prev_shift
                elif prev_start < start and start < prev_end:
                    # e.g. [[1, 5, 2]] + [2, 9, 4]
                    # [1, 5, 2] + [2, 9, 4] = [1, 1, 2] + [2, 5, 6] + [6, 9, 4]
                    collapsed.append((prev_start, start - 1, prev_shift))
                    collapsed.append((start, prev_end, prev_shift + shift))
                    start = prev_end + 1
            collapsed.append((start, end, shift))
            print(collapsed)

            # print(curr, collapsed)
        print(self.to_type, self.from_type, collapsed)
        return collapsed


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
            self.seed_ranges.append((seed_list[i], seed_list[i] + seed_list[i+1]))
        self.conversion_dict = conversion_dict
        reverse_dict = {conversion_dict[key].to_type: conversion_dict[key] for key in conversion_dict}
        key = "location"
        current_list = []
        while key in reverse_dict:
            last_conversion_dict = reverse_dict[key]
            current_list = last_conversion_dict.invert(current_list)
            key = last_conversion_dict.from_type



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
    ans = 0
    return 0

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
