from typing import Any, Optional, List, Tuple, Set, Dict
import argparse
from collections import deque
from enum import Enum 

sample_1_file_path = "test/10.sample"
sample_2_file_path = "test/10.sample2"
sample_3_file_path = "test/10.sample3"
sample_4_file_path = "test/10.sample4"
sample_5_file_path = "test/10.sample5"
input_file_path = "test/10.input"
    
class PipeMap10:
    max_row: int
    max_col: int
    pipe_map: List[str]
    starting_point: Tuple[int, int]

    def __init__(self, pipe_map: List[str], max_row: int, max_col: int):
        self.max_col = max_col
        self.max_row = max_row
        self.pipe_map = pipe_map
        for row in range(len(pipe_map)):
            for col in range(len(pipe_map[0])):
                if pipe_map[row][col] == "S":
                    self.starting_point = (col, row)
    
    def get_valid_neighbors(self, coord: Tuple[int, int]) -> List[Tuple[int, int]]:
        col, row = coord
        char = self.pipe_map[row][col]
        valid_next = []
        check_south = False
        check_north = False
        check_west = False
        check_east = False
        if char == "|":
            check_north = True
            check_south = True
        elif char == "-":
            check_west = True
            check_east = True
        elif char == "L":
            check_north = True
            check_east = True
        elif char == "J":
            check_north = True
            check_west = True
        elif char == "7":
            check_south = True
            check_west = True
        elif char == "F":
            check_south = True
            check_east = True
        elif char == ".":
            pass
        elif char == "S":
            check_south = True
            check_north = True
            check_west = True
            check_east = True

        if check_north:
            # check north
            cand = (col, row - 1)
            if row > 0 and self.pipe_map[cand[1]][cand[0]] in "|7F":
                valid_next.append(cand)
        if check_south:
            # check south
            cand = (col, row + 1)
            if row < self.max_row - 1 and self.pipe_map[cand[1]][cand[0]] in "|JL":
                valid_next.append(cand)
        if check_west:
            cand = (col - 1, row)
            if col > 0 and self.pipe_map[cand[1]][cand[0]] in "-LF":
                valid_next.append(cand)
        if check_east:
            cand = (col + 1, row)
            if col < self.max_col - 1 and self.pipe_map[cand[1]][cand[0]] in "-J7":
                valid_next.append(cand)
        return valid_next

def domain_expansion(input: PipeMap10, valid_pipes: Set[Tuple[int, int]]) -> Tuple[PipeMap10, Set[Tuple[int, int]]]:
    expanded_map = [["." for _ in range(len(input.pipe_map[0]) * 3)] for _ in range(len(input.pipe_map) * 3)]
    new_valid_pipes = set()
    for row in range(len(input.pipe_map)):
        for col in range(len(input.pipe_map[0])):
            if (col, row) not in valid_pipes:
                continue
            row_start = row * 3
            col_start = col * 3
            char = input.pipe_map[row][col]
            if char == "|":
                expanded_map[row_start + 0][col_start + 1] = "|"
                expanded_map[row_start + 1][col_start + 1] = "|"
                expanded_map[row_start + 2][col_start + 1] = "|"
                new_valid_pipes |= {(row_start + 0, col_start + 1), (row_start + 1, col_start + 1), (row_start + 2, col_start + 1)}
            elif char == "-":
                expanded_map[row_start + 1][col_start + 0] = "-"
                expanded_map[row_start + 1][col_start + 1] = "-"
                expanded_map[row_start + 1][col_start + 2] = "-"
                new_valid_pipes |= {(row_start + 1, col_start + 0), (row_start + 1, col_start + 1), (row_start + 1, col_start + 2)}
            elif char == "L":
                expanded_map[row_start + 0][col_start + 1] = "|"
                expanded_map[row_start + 1][col_start + 1] = "L"
                expanded_map[row_start + 1][col_start + 2] = "-"
                new_valid_pipes |= {(row_start + 0, col_start + 1), (row_start + 1, col_start + 1), (row_start + 1, col_start + 2)}
            elif char == "J":
                expanded_map[row_start + 0][col_start + 1] = "|"
                expanded_map[row_start + 1][col_start + 1] = "J"
                expanded_map[row_start + 1][col_start + 0] = "-"
                new_valid_pipes |= {(row_start + 0, col_start + 1), (row_start + 1, col_start + 1), (row_start + 1, col_start + 0)}
            elif char == "7":
                expanded_map[row_start + 1][col_start + 0] = "-"
                expanded_map[row_start + 1][col_start + 1] = "7"
                expanded_map[row_start + 2][col_start + 1] = "|"
                new_valid_pipes |= {(row_start + 1, col_start + 0), (row_start + 1, col_start + 1), (row_start + 2, col_start + 1)}
            elif char == "F":
                expanded_map[row_start + 1][col_start + 1] = "F"
                expanded_map[row_start + 1][col_start + 2] = "-"
                expanded_map[row_start + 2][col_start + 1] = "|"
                new_valid_pipes |= {(row_start + 1, col_start + 1), (row_start + 1, col_start + 2), (row_start + 2, col_start + 1)}
            elif char == ".":
                pass
            elif char == "S":
                expanded_map[row_start + 0][col_start + 1] = "|"
                expanded_map[row_start + 1][col_start + 0] = "-"
                expanded_map[row_start + 1][col_start + 1] = "S"
                expanded_map[row_start + 1][col_start + 2] = "-"
                expanded_map[row_start + 2][col_start + 1] = "|"
                new_valid_pipes |= {(row_start + 0, col_start + 1), (row_start + 1, col_start + 0), (row_start + 1, col_start + 1), (row_start + 1, col_start + 2), (row_start + 2, col_start + 1)}
    return PipeMap10(["".join(row) for row in expanded_map], len(expanded_map), len(expanded_map[0])), new_valid_pipes

def parse_file_day10(file_path) -> PipeMap10:
    with open(file_path, "r") as f:
        pipe_map = []
        for line in f:
            l_stripped = line.strip()
            pipe_map.append(l_stripped)
        row = len(pipe_map)
        col = len(pipe_map[0])
    pm = PipeMap10(pipe_map, row, col)
    return pm


def solve_day10_part1(input: PipeMap10) -> int:
    seen = set()
    cands = deque()
    cands.append((0, input.starting_point))
    max_dist = 0
    while cands:
        dist, cand = cands.popleft()
        if cand in seen:
            continue
        if dist > max_dist:
            max_dist = dist
        seen.add(cand)
        valid_next = input.get_valid_neighbors(cand)
        for v in valid_next:
            if v in seen:
                continue
            cands.append((dist + 1, v))
    return max_dist

class StateEnum10(Enum):
    PIPE = 1
    INSIDE = 2
    OUTSIDE = 3

def explore(cand: Tuple[int, int], input: PipeMap10, pipe_set: Set[Tuple[int, int]], seen_superset: Dict[int, StateEnum10], curr_set: Set[Tuple[int, int]]) -> Tuple[int, bool]:
    cands = deque([cand])
    valid = True
    visited = 0
    while cands:
        coord = cands.popleft()
        row, col = coord
        if row < 0 or row >= input.max_row or col < 0 or col >= input.max_col:
            valid = False
            continue
        if coord in pipe_set or coord in seen_superset:
            continue
        seen_superset.add(coord)
        curr_set.add(coord)
        visited += 1
        # check north, east, south, west
        cands.append((row, col - 1))
        cands.append((row, col + 1))
        cands.append((row - 1, col))
        cands.append((row + 1, col))
    return visited, valid

def count_insides(input: PipeMap10, inside_set: Set[Tuple[int, int]]) -> int:
    val = 0
    for row in range(input.max_row // 3):
        for col in range(input.max_col // 3):
            val += all([(row * 3 + i, col * 3 + j) in inside_set for i in range(3) for j in range(3)])
    return val

def solve_day10_part2(input: PipeMap10, debug: bool = False) -> int:
    seen = set()
    cands = deque()
    cands.append((0, input.starting_point))
    while cands:
        dist, cand = cands.popleft()
        if cand in seen:
            continue
        seen.add(cand)
        valid_next = input.get_valid_neighbors(cand)
        for v in valid_next:
            if v in seen:
                continue
            cands.append((dist + 1, v))
    new_input, new_pipes = domain_expansion(input, seen)
    if debug:
        for r in input.pipe_map:
            print(r)
        for r in new_input.pipe_map:
            print(r)
    # Seen is set of new_pipes
    seen_superset = set()
    inside_set = set()
    outside_set = set()
    for row in range(new_input.max_row):
        for col in range(new_input.max_col):
            cand = (row, col)
            if cand in seen_superset:
                continue
            else:
                curr_set = set()
                _, valid = explore(cand, new_input, new_pipes, seen_superset, curr_set)
                # print(_, valid)
                if valid:
                    inside_set |= curr_set
                else:
                    outside_set |= curr_set
    if debug:
        print()
        for row in range(new_input.max_row):
            s = ""
            for col in range(new_input.max_col):
                if (row, col) in inside_set:
                    s += "I"
                elif (row, col) in outside_set:
                    s += "O"
                else:
                    s += new_input.pipe_map[row][col]
            print(s)
    num_inside = count_insides(new_input, inside_set)
    return num_inside

def solve_day10(file_path: str, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None):
    print("---------------------------------")
    print("Input file:", file_path)
    input = parse_file_day10(file_path)
    out_part1 = solve_day10_part1(input)

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

    out_part2 = solve_day10_part2(input, debug=(expected_pt2 is not None))
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

def main_10(run_all: bool = False):
    print("Running script for day 10")
    print("Sample input")
    expected_pt1 = 4
    solve_day10(sample_1_file_path, expected_pt1=expected_pt1)
    expected_pt1 = 8
    solve_day10(sample_2_file_path, expected_pt1=expected_pt1)
    solve_day10(sample_3_file_path, expected_pt2=4)
    solve_day10(sample_4_file_path, expected_pt2=8)
    solve_day10(sample_5_file_path, expected_pt2=10)

    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day10(input_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_10(run_all=args.actual)
