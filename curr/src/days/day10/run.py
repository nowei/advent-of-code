from typing import List, Tuple, Dict
from collections import defaultdict

InputType = Tuple[List[List[int]], List[Tuple[int, int]]]
parent_path = "src/days/day10/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    grid = []
    trailheads = []
    with open(file_name, "r") as f:
        for line in f:
            grid.append([int(v) for v in line.strip() if v.isnumeric()])
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                trailheads.append((row, col))
    return grid, trailheads


def _bfs(grid, start):
    curr_layer = [start]
    seen = set()
    endings = 0
    while curr_layer:
        new_layer = []
        for row, col in curr_layer:
            if (row, col) in seen:
                continue
            seen.add((row, col))
            val = grid[row][col]
            if val == 9:
                endings += 1
            # Check cands
            _to_check = [(row + i, col) for i in range(-1, 2, 2)] + [
                (row, col + i) for i in range(-1, 2, 2)
            ]
            for n_row, n_col in _to_check:
                if (
                    n_row < 0
                    or n_row >= len(grid)
                    or n_col < 0
                    or n_col >= len(grid[0])
                ):
                    continue
                if (n_row, n_col) in seen:
                    continue
                n_val = grid[n_row][n_col]
                if n_val == val + 1:
                    new_layer.append((n_row, n_col))
        curr_layer = new_layer
    return endings


def part1(_input: InputType) -> int:
    grid, trailheads = _input
    total_paths = 0
    for line in grid:
        print(line)
    print(trailheads)
    for start in trailheads:
        total_paths += _bfs(grid, start)
    return total_paths


def _bfs_2(grid, start):
    curr_layer: Dict[Tuple[int, int], int] = {start: 1}
    seen = set()
    endings = 0
    while curr_layer:
        new_layer: Dict[Tuple[int, int], int] = defaultdict(lambda: 0)
        for row, col in curr_layer:
            val = grid[row][col]
            from_paths = curr_layer[(row, col)]
            if val == 9:
                endings += from_paths
            seen.add((row, col))
            # Check cands
            _to_check = [(row + i, col) for i in range(-1, 2, 2)] + [
                (row, col + i) for i in range(-1, 2, 2)
            ]
            for n_row, n_col in _to_check:
                if (
                    n_row < 0
                    or n_row >= len(grid)
                    or n_col < 0
                    or n_col >= len(grid[0])
                ):
                    continue
                n_val = grid[n_row][n_col]
                if n_val == val + 1:
                    new_layer[(n_row, n_col)] += from_paths
        curr_layer = new_layer
    return endings


def part2(_input: InputType) -> int:
    grid, trailheads = _input
    total_paths = 0
    for line in grid:
        print(line)
    print(trailheads)
    for start in trailheads:
        total_paths += _bfs_2(grid, start)
    return total_paths


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
