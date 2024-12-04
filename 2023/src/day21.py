from typing import Any, Optional, List, Tuple, Dict, Set
from collections import defaultdict
import argparse

sample_file_path = "test/21.sample"
input_file_path = "test/21.input"

class Setting21:

    grid: List[str]
    possible_steps: Dict[str, Set[Tuple[int, int]]]
    start: Tuple[int, int]

    def __init__(self, grid):
        self.grid = grid
        self.get_possible_steps()
        self.start = None
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == "S":
                    self.start = (row, col)
                    break
            if self.start:
                break
        self.max_rows = len(grid)
        self.max_cols = len(grid[0])
    
    def get_possible_steps(self):
        possible_steps = defaultdict(lambda: set())
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if row > 0 and self.grid[row - 1][col] != "#":
                    possible_steps[(row, col)].add((row - 1, col))
                if row < len(self.grid) - 1 and self.grid[row + 1][col] != "#":
                    possible_steps[(row, col)].add((row + 1, col))
                if col > 0 and self.grid[row][col - 1] != "#":
                    possible_steps[(row, col)].add((row, col - 1))
                if col < len(self.grid[0]) - 1 and self.grid[row][col + 1] != "#":
                    possible_steps[(row, col)].add((row, col + 1))
        self.possible_steps = possible_steps
    
    def visualize(self, curr: Set[Tuple[int, int]]):
        for row in range(len(self.grid)):
            print("".join(["O" if (row, col) in curr else self.grid[row][col] for col in range(len(self.grid[0]))]))

def parse_file_day21(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    m = []
    for line in lines:
        curr = line.strip()
        m.append(curr)
    return Setting21(m)

def solve_day21_part1(input: Setting21, steps: int = 64) -> int:
    prevprev = set()
    prev = set()
    curr = set([input.start])
    # In reality we only need to evaluate step[i] that is not in step[i - 1]
    for i in range(steps):
        cand = prev.copy()
        for new in curr.difference(prevprev):
            cand |= input.possible_steps[new]
        curr, prev, prevprev = cand, curr, prev
        # input.visualize(curr)
    return len(curr)

def solve_day21_part2(input: Setting21, steps=26501365) -> int:
    # number of steps until saturation on one map can give us a good 
    prevprev = set()
    prev = set()
    curr = set([input.start])
    # In reality we only need to evaluate step[i] that is not in step[i - 1]
    graphs = []
    # fill a single square
    for i in range(200):
        cand = prev.copy()
            
        for new in curr.difference(prevprev):
            cand |= input.possible_steps[new]
        # for row, col in curr.difference(prevprev):
        #     # check every direction
        #     if input.grid[(row - 1) % input.max_rows][col % input.max_cols] != "#":
        #         cand.add((row - 1, col))
        #     if input.grid[(row + 1) % input.max_rows][col % input.max_cols] != "#":
        #         cand.add((row + 1, col))
        #     if input.grid[row % input.max_rows][(col - 1) % input.max_cols] != "#":
        #         cand.add((row, col - 1))
        #     if input.grid[row % input.max_rows][(col + 1) % input.max_cols] != "#":
        #         cand.add((row, col + 1))
        # print("diff is", curr.difference(prevprev))
        # print(prevprev)
        # print(prev)
        # print(curr)
        # print(cand)
        curr, prev, prevprev = cand, curr, prev
        # input.visualize(curr)
        graphs.append(len(curr))
    odd_filled = graphs[input.max_rows - 1]
    even_filled = graphs[input.max_rows]
    even_corners = even_filled - graphs[64 - 1]
    odd_corners = odd_filled - graphs[64]
    # n is the number of squares walked
    n = steps // input.max_rows
    print(n)

    return (n + 1) * (n + 1) * odd_filled + (n * n) * even_filled - (n + 1) * odd_corners + n * even_corners

def solve_day21(input: Setting21, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None, steps: Optional[int] = None, steps2: Optional[int] = None):
    if steps:
        out_part1 = solve_day21_part1(input, steps)
    else:
        out_part1 = solve_day21_part1(input)

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

    if steps2:
        out_part2 = solve_day21_part2(input, steps2)
    else:
        out_part2 = solve_day21_part2(input)
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

def main_21(run_all: bool = False, example: Optional[str] = None, answer_only: bool = False):
    if not answer_only:
        if example:
            print("Testing input from cmd line")
            input = parse_file_day21("", example=example)
            solve_day21(input)
            exit(0)

        print("Running script for day 21")
        print("Sample input")
        print("---------------------------------")
        expected_out_part1 = 16
        expected_out_part2 = None
        print("Input file:", sample_file_path)
        input = parse_file_day21(sample_file_path)
        solve_day21(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2, steps=6, steps2=500)

    if answer_only or run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day21(input_file_path)
        solve_day21(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    parser.add_argument('-e', '--example')
    parser.add_argument('-o', '--answer_only', action='store_true')
    args = parser.parse_args()
    main_21(run_all=args.actual, example=args.example, answer_only=args.answer_only)
