from typing import Any, Optional, List, Dict, Tuple
from collections import defaultdict
import argparse

sample_file_path = "test/16.sample"
input_file_path = "test/16.input"

class Direction16:
    seen: Dict[str, int]

    def __init__(self):
        self.seen = defaultdict(lambda: 0)

    def __repr__(self):
        total = 0
        for k, v in self.seen.items():
            total += v
        if total == 0:
            return 0
        elif total == 1:
            return k
        else:
            return total

class Setting16:
    map: List[List[str]]

    def __init__(self, map):
        self.map = map
        # Populate the energized list
    
    def get_energy(self, init):
        beams = [init]
        energized_list = defaultdict(lambda: Direction16())
        spot_map = {
            "/": {
                "N": ["E"],
                "E": ["N"],
                "S": ["W"],
                "W": ["S"],
            },
            "\\": {
                "N": ["W"],
                "W": ["N"],
                "S": ["E"],
                "E": ["S"],
            },
            "-": {
                "N": ["W", "E"],
                "S": ["W", "E"],
                "W": ["W"],
                "E": ["E"],
            },
            "|": {
                "N": ["N"],
                "S": ["S"],
                "W": ["N", "S"],
                "E": ["N", "S"],
            },
            ".": {
                "N": ["N"],
                "S": ["S"],
                "W": ["W"],
                "E": ["E"],
            },
        }
        seen = set()
        while beams:
            new_beams = []
            for b in beams:
                if b in seen:
                    continue
                seen.add(b)
                row, col, dir = b
                if dir == "N":
                    row -= 1
                elif dir == "E":
                    col += 1
                elif dir == "S":
                    row += 1
                else: # dir == "W"
                    col -= 1
                if row < 0 or row >= len(self.map):
                    continue
                if col < 0 or col >= len(self.map[0]):
                    continue
                spot = self.map[row][col]
                for new_dir in spot_map[spot][dir]:
                    new_beams.append((row, col, new_dir))
                energized_list[(row, col)].seen[dir] += 1
            beams = new_beams
        return len(energized_list)

def parse_file_day16(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    m = []
    for line in lines:
        m.append([c for c in line.strip()])
    return Setting16(m)

def solve_day16_part1(input: Setting16) -> int:
    return input.get_energy((0, -1, "E"))

def solve_day16_part2(input: Setting16) -> int:
    best = 0
    borders = []
    for i in range(len(input.map)):
        borders.extend([(i, -1, "E"), (i, len(input.map[0]), "W")])
    for i in range(len(input.map[0])):
        borders.extend([(len(input.map), i, "N"), (-1, i, "S")])

    for cand in borders:
        best = max(best, input.get_energy(cand))
    return best

def solve_day16(input: Any, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None):
    out_part1 = solve_day16_part1(input)

    if expected_pt1 is not None:
        if out_part1 != expected_pt1:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_pt1)
        else:
            print("Sample matched")
    print("Part 1 result:")
    print(out_part1)
    print()

    out_part2 = solve_day16_part2(input)
    if expected_pt2 is not None:
        if out_part2 != expected_pt2:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_pt2)
        else:
            print("Sample matched")
    print("Part 2 result:")
    print(out_part2)
    print()

def main_16(run_all: bool = False, example: Optional[str] = None):
    if example:
        print("Testing input from cmd line")
        input = parse_file_day16("", example=example)
        solve_day16(input)
        exit(0)

    print("Running script for day 16")
    print("Sample input")
    print("---------------------------------")
    expected_out_part1 = 46
    expected_out_part2 = 51
    print("Input file:", sample_file_path)
    input = parse_file_day16(sample_file_path)
    solve_day16(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day16(input_file_path)
        solve_day16(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_16(run_all=args.actual)
