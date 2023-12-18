from collections import defaultdict
from typing import Any, Optional, List, Tuple
import argparse

sample_file_path = "test/18.sample"
input_file_path = "test/18.input"

class Instruction18:
    dir: str
    dist: int
    color: str

    def __init__(self, dir, dist, color):
        self.dir = dir
        self.dist = dist
        self.color = color

class Setting18:
    instructions: List[Instruction18]

    def __init__(self, inst):
        self.instructions = inst
    
    def process_fill(self) -> int:
        # note that a smarter way to do this without doing a fill flood algorithm would be
        # to count the number of consecutive pieces to determine if it's inside or outside the shape,
        # e.g. .##..#.##..##... would have O##II#O##II##OOO based on the the crossings
        # e.g. .##########... would have no crossings, so we only have to check the first # and last # in the rows
        curr_row, curr_col = 0, 0
        m = defaultdict(lambda: list())
        m[0].append(0)
        for inst in self.instructions:
            dir, dist, color = inst.dir, inst.dist, inst.color
            row_diff = 0
            col_diff = 0
            if dir == "U":
                row_diff = -1
            elif dir == "D":
                row_diff = 1
            elif dir == "L":
                col_diff = -1
            else: # dir == "R"
                col_diff = 1
            # go up, subtract
            for _ in range(dist):
                curr_row += row_diff
                curr_col += col_diff
                m[curr_row].append(curr_col)
        # draw
        max_row = max(m.keys())
        min_row = min(m.keys())
        max_col = max([max(m[c]) for c in m])
        min_col = min([min(m[c]) for c in m])
        drawing = [["." for _ in range(min_col, max_col + 1)] for _ in range(min_row, max_row + 1)]
        for row in m:
            for c in m[row]:
                drawing[row - min_row][c - min_col] = "#"
        for line in drawing:
            print("".join(line))
        print()
        for row in range(1, len(drawing) - 1):
            inside = False
            seen_above = False
            seen_below = False
            if drawing[row][0] == "#":
                if drawing[row - 1][0] == "#": seen_above = True
                if drawing[row + 1][0] == "#": seen_below = True
            if seen_above and seen_below:
                inside = True
                seen_above = False
                seen_below = False
            for col in range(1, len(drawing[row])):
                if drawing[row][col] == "#":
                    if drawing[row - 1][col] == "#": seen_above = True
                    if drawing[row + 1][col] == "#": seen_below = True
                    if seen_above and seen_below:
                        inside = not inside
                        seen_above = False
                        seen_below = False
                else: # drawing[row][col] == ".":
                    if inside:
                        drawing[row][col] = "#"
                    else:
                        seen_above = False
                        seen_below = False
        for line in drawing:
            print("".join(line))
        return sum([row.count("#") for row in drawing])

    def reversed_instructions_process(self):
        # We use the shoelace formula, also known as Gauss's area formula or the surveyor's formula
        # https://en.wikipedia.org/wiki/Shoelace_formula

        # We also use Pick's theorem:
        # https://en.wikipedia.org/wiki/Pick%27s_theorem
        curr_row = 0
        curr_col = 0
        coords = [(curr_row, curr_col)]
        perimeter_dist = 0 # Need to consider the contribution of the perimeter
        for inst in self.instructions:
            _, _, color = inst.dir, inst.dist, inst.color
            dist = int(color[0:5], 16)
            dir_spec = color[5]
            if dir_spec == "0": dir = "R"
            elif dir_spec == "1": dir = "D"
            elif dir_spec == "2": dir = "L"
            elif dir_spec == "3": dir = "U"
            row_diff = 0
            col_diff = 0
            if dir == "U":
                row_diff = -1
            elif dir == "D":
                row_diff = 1
            elif dir == "L":
                col_diff = -1
            else: # dir == "R"
                col_diff = 1
            curr_row += row_diff * dist
            curr_col += col_diff * dist
            perimeter_dist += abs(row_diff * dist) + abs(col_diff * dist)
            coords.append((curr_row, curr_col))
        total = 0
        for i in range(1, len(coords)):
            prev_y, prev_x = coords[i - 1]
            curr_y, curr_x = coords[i]
            # x1y2 - x2y1
            total += (prev_x * curr_y) - (curr_x * prev_y)
        prev_y, prev_x = coords[-1]
        curr_y, curr_x = coords[0]
        total += (prev_x * curr_y) - (curr_x * prev_y)
        # perimeter_dist # 87716969654406
        return total / 2 + perimeter_dist / 2 + 1
            
            

def parse_file_day18(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    instructions = []
    for line in lines:
        dir, dist, color = line.strip().split()
        instructions.append(Instruction18(dir, int(dist), color.strip("(#)")))

    return Setting18(instructions)

def solve_day18_part1(input: Setting18) -> int:
    return input.process_fill()

def solve_day18_part2(input: Setting18) -> int:
    return input.reversed_instructions_process()

def solve_day18(input: Setting18, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None):
    out_part1 = solve_day18_part1(input)

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

    out_part2 = solve_day18_part2(input)
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

def main_18(run_all: bool = False, example: Optional[str] = None):
    if example:
        print("Testing input from cmd line")
        input = parse_file_day18("", example=example)
        solve_day18(input)
        exit(0)

    print("Running script for day 18")
    print("Sample input")
    print("---------------------------------")
    expected_out_part1 = 62
    expected_out_part2 = 952408144115
    print("Input file:", sample_file_path)
    input = parse_file_day18(sample_file_path)
    solve_day18(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day18(input_file_path)
        solve_day18(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_18(run_all=args.actual)
