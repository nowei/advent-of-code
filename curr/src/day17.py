from typing import Any, Optional, List, Tuple
import heapq
import argparse

sample_file_path = "test/17.sample"
input_file_path = "test/17.input"

class Setting17:
    map: List[List[int]]

    def __init__(self, map):
        self.map = map
        self.max_row = len(map)
        self.max_col = len(map[0])
    
    def solve(self, start: Tuple[int, int], end: Tuple[int, int], min_straight: int = 1, max_straight: int = 3) -> int:
        # tuples will be [cost, row, col, dir, straight]
        heap = [(0, start, 'I', max_straight)]

        new_dir_map = {
            "N": "WNE",
            "E": "NES",
            "S": "ESW",
            "W": "SWN",
            "I": "SWNE",
        }

        move_diff_map = {
            "N": [-1, 0],
            "E": [0, 1],
            "S": [1, 0],
            "W": [0, -1],
        }

        def get_next(cand: Tuple[int, Tuple[int, int], str, int]) -> List[Tuple[int, Tuple[int, int], str, int]]:
            cost, curr_pos, dir, curr_straight = cand
            curr_row, curr_col = curr_pos
            next_cands = []
            # Go forward and add options from there
            new_dirs = new_dir_map[dir]
            for d in new_dirs:
                row_diff, col_diff = move_diff_map[d]
                if d != dir:
                    row_diff *= min_straight
                    col_diff *= min_straight
                new_row = curr_row + row_diff
                new_col = curr_col + col_diff
                if new_row < 0 or new_row > self.max_row - 1:
                    continue
                if new_col < 0 or new_col > self.max_col - 1:
                    continue

                new_pos = (new_row, new_col)
                if d != dir:
                    new_cost = cost
                    if row_diff > 0:
                        for i in range(1, row_diff + 1):
                            new_cost += self.map[curr_row + i][curr_col]
                    else:
                        for i in range(-1, row_diff - 1, -1):
                            new_cost += self.map[curr_row + i][curr_col]
                    if col_diff > 0:
                        for i in range(1, col_diff + 1):
                            new_cost += self.map[curr_row][curr_col + i]
                    else:
                        for i in range(-1, col_diff - 1, -1):
                            new_cost += self.map[curr_row][curr_col + i]
                else:
                    new_cost = cost + self.map[new_row][new_col]
                if d == dir:
                    if curr_straight > 0:
                        next_cands.append((new_cost, new_pos, d, curr_straight - 1))
                else:
                    next_cands.append((new_cost, new_pos, d, max_straight - min_straight))
            return next_cands

        seen = set()
        from_map = {}
        while heap:
            cand = heapq.heappop(heap)
            if cand[1:] in seen:
                continue
            seen.add(cand[1:])
            if cand[1] == end:
                break
            next_cands = get_next(cand)
            
            for c in next_cands:
                from_map[c] = cand
                heapq.heappush(heap, c)
        print(cand)
        result_from = {}
        result_cost = cand[0]
        while cand in from_map:
            result_from[cand[1]] = cand[-2]
            cand = from_map[cand]
        for row in range(len(self.map)):
            v = ""
            for col in range(len(self.map[0])):
                if (row, col) not in result_from:
                    v += "."
                    continue
                dir = result_from[(row, col)]
                if dir == "N":
                    v += "^"
                elif dir == "S":
                    v += "v"
                elif dir == "E":
                    v += ">"
                elif dir == "W":
                    v += "<"
            print(v)

        return result_cost


def parse_file_day17(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    m = []
    for line in lines:
        m.append([int(c) for c in line.strip()])
    return Setting17(m)

def solve_day17_part1(input: Setting17) -> int:
    return input.solve((0, 0), (input.max_row - 1, input.max_col - 1))

def solve_day17_part2(input: Setting17) -> int:
    return input.solve((0, 0), (input.max_row - 1, input.max_col - 1), min_straight=4, max_straight=10)

def solve_day17(input: Any, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None):
    out_part1 = solve_day17_part1(input)

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

    out_part2 = solve_day17_part2(input)
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

def main_17(run_all: bool = False, example: Optional[str] = None):
    if example:
        print("Testing input from cmd line")
        input = parse_file_day17("", example=example)
        solve_day17(input)
        exit(0)

    print("Running script for day 17")
    print("Sample input")
    print("---------------------------------")
    expected_out_part1 = 102
    expected_out_part2 = 94
    print("Input file:", sample_file_path)
    input = parse_file_day17(sample_file_path)
    solve_day17(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day17(input_file_path)
        solve_day17(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_17(run_all=args.actual)
