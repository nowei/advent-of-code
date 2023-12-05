from typing import Any, List, Dict, Tuple
import argparse
import bisect

sample_file_path = "test/05.sample"
input_file_path = "test/05.input"
expected_out_part1 = 35
expected_out_part2 = None

class Conversion_05:
    from_type: str
    to_type: str
    ranges: List[Tuple[int, int, int]]
    converted_range: Dict[Tuple[int, int], int]

    def __init__(self, from_type: str, to_type: str, ranges: List[Tuple[int, int, int]]) -> None:
        self.from_type = from_type
        self.to_type = to_type
        self.ranges = ranges
        self.converted_range = {}
        for r in self.ranges:
            source, destination, range_length = r
            self.converted_range[(source, source + range_length - 1)] = destination - source

    def convert(self, number: int):
        # Right binary search so that the index can be the number
        # We use filler numbers for the converted range and range length so it only pays attention
        # to the first number.
        insert_index = bisect.bisect_right(self.ranges, (number, -float('inf'), -float('inf')))
        prev_range_index = insert_index - 1
        # return number as the index because there is no converted range
        if prev_range_index < 0:
            return number
        source, destination, range_length = self.ranges[prev_range_index]
        from_range_end = source + range_length
        if number >= source and from_range_end > number:
            diff = number - source
            return destination + diff
        else:
            return number
    
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
    def invert(self, other_ranges: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], int]:
        print(self.converted_range)
        print(other_ranges)
        new_ranges = {}
        self_ranges = self.converted_range
        sorted_other_keys = sorted(other_ranges.keys())
        sorted_self_keys = sorted(self.converted_range.keys())
        other_idx = 0
        idx = 0
        # We want to move up one index at a time, but only update the indicies when we 
        # have consumed all the values in the range
        while other_idx < len(sorted_other_keys) and idx < len(sorted_self_keys):
            # Possible cases where:
            # a            b
            # |----self----|
            # and 
            # c         d
            # |--other--|
            # * there is overlap
            # Cases:
            #   * End of self is in other -> consume self, keep other
            #   |---self---|
            #        |---other---|
            #   * Start of self is in other -> consume other, keep self
            #        |---self---|
            #   |---other---|
            #   * Self is inside of other -> consume other up to the end of self, update self
            #     |--self--|
            #   |---other---|
            #   * Other is inside of self -> consume self up to other, update other
            #     |---self---|
            #       |-other-|
            #   * They match exactly -> update both
            #     |---self---|
            #     |--other---|
            # * there is no overlap -> add smallest range to new_ranges and add
            # End of self is less than the start of other, so we add self
            # |----self----|
            #                |--other--|
            # Otherwise, we add other
            #                |--self--|
            # |----other----|
            self_key = sorted_self_keys[idx]
            a, b = self_key
            self_diff = self_ranges[self_key]
            other_key = sorted_other_keys[other_idx]
            c, d = other_key
            other_diff = other_ranges[other_key]
            if a == c and b == d:
                diff = self_diff + other_diff
                new_ranges[self_key] = diff
                idx += 1
                other_idx += 1
            elif 
            else:
                if b < c:
                    new_ranges[self_key] = self_ranges[self_key]
                    idx += 1
                else:
                    new_ranges[other_key] = other_ranges[other_key]
                    other_idx += 1
        while other_idx < len(sorted_other_keys):
            key = sorted_other_keys[other_idx]
            new_ranges[key] = sorted_other_keys[key]
        while idx < len(sorted_self_keys):
            key = sorted_self_keys[idx]
            new_ranges[key] = sorted_self_keys[key]
        return new_ranges

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
            self.seed_ranges.append((seed_list[i],seed_list[i] + seed_list[i+1]))
        self.conversion_dict = conversion_dict
        reverse_dict = {conversion_dict[key].to_type: conversion_dict[key] for key in conversion_dict}
        last_conversion_dict = reverse_dict["location"]
        reverse_dict[last_conversion_dict.from_type].invert(last_conversion_dict.converted_range)



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

def solve_day05_part2(input: Any) -> Any:
    return None

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
