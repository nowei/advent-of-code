from typing import Any, Optional, List, Tuple
from collections import defaultdict, deque
import argparse

import sys

sys.setrecursionlimit(10000)

sample_file_path = "test/23.sample"
input_file_path = "test/23.input"


class Setting23:
    grid: List[str]
    start: Tuple[int, int]
    end: Tuple[int, int]
    row_max: int
    col_max: int

    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.row_max = len(self.grid)
        self.col_max = len(self.grid[0])

    def longest_path(self, steep=True):
        seen = set()
        path = [self.start]
        heuristic = {}
        curr_best = [0]

        def consider(path: List[Tuple[int, int]]):
            # check all directions for if we can go, left, right, up, or down, if v, go two in that direciton
            if path[-1] == self.end:
                curr_len = len(path)
                for p in path:
                    heuristic[p] = curr_len
                return curr_len
            row, col = path[-1]
            # if path[-1] in heuristic and len(path) < heuristic[path[-1]]:
            #     return 0
            checks = []
            # check north
            curr = (row - 1, col)
            if curr not in seen:
                c = self.grid[curr[0]][curr[1]]
                if c != "#" and (not steep or c != "v"):
                    if steep and c == "^":
                        checks.append([curr, (row - 2, col)])
                    else:
                        checks.append([curr])
            # check south
            curr = (row + 1, col)
            if curr not in seen:
                c = self.grid[curr[0]][curr[1]]
                if c != "#" and (not steep or c != "^"):
                    if steep and c == "v":
                        checks.append([curr, (row + 2, col)])
                    else:
                        checks.append([curr])

            # check east
            curr = (row, col + 1)
            if curr not in seen:
                c = self.grid[curr[0]][curr[1]]
                if c != "#" and (not steep or c != "<"):
                    if steep and c == ">":
                        checks.append([curr, (row, col + 2)])
                    else:
                        checks.append([curr])
            # check west
            curr = (row, col - 1)
            if curr not in seen:
                c = self.grid[curr[0]][curr[1]]
                if c != "#" and (not steep or c != ">"):
                    if steep and c == "<":
                        checks.append([curr, (row, col - 2)])
                    else:
                        checks.append([curr])

            best = 0
            for dir in checks:
                for step in dir:
                    path.append(step)
                    seen.add(step)
                cand = consider(path)
                if cand > best:
                    best = cand
                    if best > curr_best[0]:
                        curr_best[0] = best
                        print(curr_best[0])
                for step in dir:
                    path.pop()
                    seen.remove(step)
            return best

        best = consider(path)
        return best - 1

    def junction_search(self):
        junctions = set()

        for row in range(1, self.row_max - 1):
            for col in range(1, self.col_max - 1):
                # if at least 3 adjacent is not "#"
                if self.grid[row][col] == "#":
                    continue
                adj = sum(
                    [
                        self.grid[row][col - 1] != "#",
                        self.grid[row][col + 1] != "#",
                        self.grid[row - 1][col] != "#",
                        self.grid[row + 1][col] != "#",
                    ]
                )
                if adj >= 3:
                    junctions.add((row, col))
        junctions.add(self.end)

        main_cand = deque([self.start])
        # go to reachable junctions
        seen = set()
        pairwise_dist = defaultdict(lambda: {})
        seen_junctions = set([self.start])
        while len(main_cand) != 0:
            curr_junction = main_cand.popleft()
            cand = deque([(curr_junction[0], curr_junction[1], 0)])
            seen_junctions.add(curr_junction)
            while cand:
                row, col, dist = cand.popleft()
                if row < 0 or col < 0 or row >= self.row_max or col >= self.col_max:
                    continue
                if (row, col) in seen_junctions and (row, col) != curr_junction:
                    if (
                        curr_junction not in pairwise_dist
                        or (row, col) not in pairwise_dist[curr_junction]
                        or pairwise_dist[curr_junction][(row, col)] < dist
                    ):
                        pairwise_dist[curr_junction][(row, col)] = dist
                        pairwise_dist[(row, col)][curr_junction] = dist
                if (row, col) in seen and (row, col) not in seen_junctions:
                    continue
                # check, north, east, south, west
                if (row, col) in junctions and (row, col) != curr_junction:
                    main_cand.append((row, col))
                    pairwise_dist[curr_junction][(row, col)] = dist
                    pairwise_dist[(row, col)][curr_junction] = dist
                else:
                    if (
                        (row - 1, col) not in seen
                        and row - 1 > 0
                        and self.grid[row - 1][col] != "#"
                    ):
                        cand.append((row - 1, col, dist + 1))
                    if (
                        (row + 1, col) not in seen
                        and row + 1 < self.row_max
                        and self.grid[row + 1][col] != "#"
                    ):
                        cand.append((row + 1, col, dist + 1))
                    if (
                        (row, col + 1) not in seen
                        and col + 1 < self.col_max
                        and self.grid[row][col + 1] != "#"
                    ):
                        cand.append((row, col + 1, dist + 1))
                    if (
                        (row, col - 1) not in seen
                        and col - 1 > 0
                        and self.grid[row][col - 1] != "#"
                    ):
                        cand.append((row, col - 1, dist + 1))
                    seen.add((row, col))
        for row in range(self.row_max):
            print(
                "".join(
                    [
                        self.grid[row][col] if (row, col) not in seen else "O"
                        for col in range(self.col_max)
                    ]
                )
            )
        vertices = junctions
        edges = pairwise_dist
        seen = set([self.start])
        print(self.end)

        def dfs(path, curr_val):
            if path[-1] == self.end:
                return curr_val
            best = 0
            for cand in edges[path[-1]]:
                if cand in seen:
                    continue
                seen.add(cand)
                best = max(best, dfs(path + [cand], curr_val + edges[path[-1]][cand]))
                seen.remove(cand)
            return best

        return dfs([self.start], 0)


def parse_file_day23(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()

    map_list = []
    first = None
    for line in lines:
        curr = line.strip()
        if not first:
            first = line
        map_list.append(curr)
    last = curr
    start = (0, first.index("."))
    end = (len(map_list) - 1, last.index("."))
    return Setting23(map_list, start, end)


def solve_day23_part1(input: Setting23) -> int:
    return input.longest_path()


def solve_day23_part2(input: Setting23) -> int:
    return input.junction_search()


def solve_day23(
    input: Setting23,
    expected_pt1: Optional[int] = None,
    expected_pt2: Optional[int] = None,
):
    out_part1 = solve_day23_part1(input)

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

    out_part2 = solve_day23_part2(input)
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


def main_23(
    run_all: bool = False, example: Optional[str] = None, answer_only: bool = False
):
    if not answer_only:
        if example:
            print("Testing input from cmd line")
            input = parse_file_day23("", example=example)
            solve_day23(input)
            exit(0)

        print("Running script for day 23")
        print("Sample input")
        print("---------------------------------")
        expected_out_part1 = 94
        expected_out_part2 = 154
        print("Input file:", sample_file_path)
        input = parse_file_day23(sample_file_path)
        solve_day23(
            input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2
        )

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day23(input_file_path)
        solve_day23(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--actual", action="store_true")
    parser.add_argument("-e", "--example")
    parser.add_argument("-o", "--answer-only", action="store_true")
    args = parser.parse_args()
    main_23(run_all=args.actual, example=args.example, answer_only=args.answer_only)
