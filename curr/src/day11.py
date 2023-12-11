from typing import Any, Optional, List, Set
import argparse

sample_file_path = "test/11.sample"
input_file_path = "test/11.input"

class Galaxy11:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other: "Galaxy11"):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def scaled_dist(self, other: "Galaxy11", galaxy_scaling=1, empty_galaxy_col=[], empty_galaxy_row=[]):
        x_i = min(self.x, other.x)
        x_o = max(self.x, other.x)
        y_i = min(self.y, other.y)
        y_o = max(self.y, other.y)
        x_empties = sum(1 for x in range(x_i, x_o) if x in empty_galaxy_col)
        y_empties = sum(1 for y in range(y_i, y_o) if y in empty_galaxy_row)
        return (x_o - x_i - x_empties + x_empties * galaxy_scaling) + (y_o - y_i - y_empties + y_empties * galaxy_scaling)

class Galaxies11:
    orig_map: List[str]
    empty_galaxy_col: Set[int]
    empty_galaxy_row: Set[int]
    galaxies: List[Galaxy11]
    expanded_row_max: int
    expanded_col_max: int
    expanded_map: List[str]
    expanded_galaxies: List[Galaxy11]

    def __init__(self, orig_map):
        self.orig_map = orig_map
        # determine which rows need to be expanded

        expansion_rows = set()
        expansion_cols = set()
        for i in range(len(orig_map)):
            if all([val == "." for val in orig_map[i]]):
                expansion_rows.add(i)
        
        for i in range(len(orig_map[0])):
            if all([val == "." for j in range(len(orig_map)) for val in orig_map[j][i]]):
                expansion_cols.add(i)
        
        print(expansion_rows)
        print(expansion_cols)
        self.empty_galaxy_col = expansion_cols
        self.empty_galaxy_row = expansion_rows
        galaxies = []
        for i in range(len(orig_map)):
            for j in range(len(orig_map[0])):
                if orig_map[i][j] == "#":
                    galaxies.append(Galaxy11(j, i))
        self.galaxies = galaxies
        new_row_max = len(orig_map) + len(expansion_rows)
        new_col_max = len(orig_map[0]) + len(expansion_cols)

        expanded_map = []
        for i in range(len(orig_map)):
            if i in expansion_rows:
                expanded_map.append(["." for _ in range(new_col_max)])
                expanded_map.append(["." for _ in range(new_col_max)])
                continue
            curr = ""
            for j in range(len(orig_map[0])):
                if j in expansion_cols:
                    curr += ".."
                else:
                    curr += orig_map[i][j]
            expanded_map.append(curr)
        self.expanded_map = expanded_map
        self.row_max = new_row_max
        self.col_max = new_col_max
        expanded_galaxies = []
        for i in range(len(expanded_map)):
            for j in range(len(expanded_map[0])):
                if expanded_map[i][j] == "#":
                    expanded_galaxies.append(Galaxy11(j, i))
        self.expanded_galaxies = expanded_galaxies

def parse_file_day11(file_path) -> Galaxies11:
    with open(file_path, "r") as f:
        lines = []
        for line in f:
            lines.append(line.strip())
    
        g = Galaxies11(lines)
    return g

def solve_day11_part1(input: Galaxies11) -> int:
    ans = 0
    for i in range(len(input.expanded_galaxies) - 1):
        for j in range(i + 1, len(input.expanded_galaxies)):
            ans += input.expanded_galaxies[i].dist(input.expanded_galaxies[j])
    return ans

def solve_day11_part2(input: Galaxies11, scaling = 1) -> int:
    ans = 0
    for i in range(len(input.galaxies) - 1):
        for j in range(i + 1, len(input.galaxies)):
            ans += input.galaxies[i].scaled_dist(input.galaxies[j], scaling, input.empty_galaxy_col, input.empty_galaxy_row)
    return ans

def solve_day11(file_path: str, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None):
    print("---------------------------------")
    print("Input file:", file_path)
    input = parse_file_day11(file_path)
    out_part1 = solve_day11_part1(input)

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

    if expected_pt2:
        out_part2 = solve_day11_part2(input, scaling=100)
    else:
        out_part2 = solve_day11_part2(input, scaling=1000000)
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

def main_11(run_all: bool = False):
    print("Running script for day 11")
    print("Sample input")
    expected_out_part1 = 374
    expected_out_part2 = 8410
    solve_day11(sample_file_path, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day11(input_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_11(run_all=args.actual)
