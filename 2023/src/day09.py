from typing import Any, List
import argparse

sample_file_path = "test/09.sample"
input_file_path = "test/09.input"
expected_out_part1 = 114
expected_out_part2 = 2

class OasisReading:
    reading: List[int]

    def __init__(self, reading):
        self.reading = reading
    
    def get_next(self, before: bool = False) -> int:
        per_layer_diffs = []
        layer = self.reading
        while any([val != 0 for val in layer]):
            next_layer = []
            for i in range(1, len(layer)):
                diff = layer[i] - layer[i - 1]
                next_layer.append(diff)
            per_layer_diffs.append(layer)
            layer = next_layer
        per_layer_diffs.append(layer)
        prev_diff = 0
        if not before:
            for layer in per_layer_diffs[::-1]:
                prev_diff = layer[-1] + prev_diff
        else:
            for layer in per_layer_diffs[::-1]:
                prev_diff = layer[0] - prev_diff
        return prev_diff

def parse_file_day09(file_path) -> List[OasisReading]:
    readings = []
    with open(file_path, "r") as f:
        for line in f:
            reading = [int(num) for num in line.strip().split()]
            readings.append(OasisReading(reading))
    return readings

def solve_day09_part1(input: List[OasisReading]) -> int:
    ans = 0
    for reading in input:
        ans += reading.get_next(before=False)
    return ans

def solve_day09_part2(input: List[OasisReading]) -> int:
    ans = 0
    for reading in input:
        ans += reading.get_next(before=True)
    return ans

def solve_day09(file_path: str, check_out: bool):
    input = parse_file_day09(file_path)
    out_part1 = solve_day09_part1(input)

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

    out_part2 = solve_day09_part2(input)
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

def main_09(run_all: bool = False):
    print("Running script for day 09")
    print("Sample input")
    solve_day09(sample_file_path, check_out=True)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day09(input_file_path, check_out=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_09(run_all=args.actual)
