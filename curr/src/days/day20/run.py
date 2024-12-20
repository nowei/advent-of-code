from typing import List, Tuple, Dict
from collections import Counter

InputType = Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]
parent_path = "src/days/day20/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    grid = []
    with open(file_name, "r") as f:
        for line in f:
            grid.append(list(line.strip()))
    start = (0, 0)
    end = (0, 0)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "S":
                start = (row, col)
            elif grid[row][col] == "E":
                end = (row, col)
    return grid, start, end


def walk(
    grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]
) -> List[Tuple[int, int]]:
    path = [start]
    while path[-1] != end:
        row, col = path[-1]
        for d_row, d_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            n_row = d_row + row
            n_col = d_col + col
            if grid[n_row][n_col] == "#":
                continue
            elif len(path) >= 2 and path[-2] == (n_row, n_col):
                continue
            else:
                break
        path.append((n_row, n_col))
    return path


def find_cheats(grid: List[List[str]], path: List[Tuple[int, int]]) -> Dict[int, int]:
    cheats: Dict[int, int] = Counter()
    path_idx_map = {p: len(path) - i - 1 for i, p in enumerate(path)}
    seen = set()
    for curr in path:
        # Check each direction
        row, col = curr
        curr_steps_to_end = path_idx_map[curr]
        seen.add(curr)
        for d_row, d_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            n_row = d_row + row
            n_col = d_col + col
            if grid[n_row][n_col] in seen:
                continue
            nn_row = 2 * d_row + row
            nn_col = 2 * d_col + col
            if nn_row < 0 or nn_row >= len(grid):
                continue
            if nn_col < 0 or nn_col >= len(grid[0]):
                continue
            if (nn_row, nn_col) in seen:
                continue
            if grid[n_row][n_col] == "#" and grid[nn_row][nn_col] != "#":
                new_pos_steps_to_end = path_idx_map[(nn_row, nn_col)]
                steps_saved = curr_steps_to_end - new_pos_steps_to_end - 2
                cheats[steps_saved] += 1
    return cheats


def part1(_input: InputType) -> int:
    grid, start, end = _input
    path = walk(grid, start, end)
    cheats = find_cheats(grid, path)
    print(sorted(cheats.items()))
    num_cheats = 0
    for key, skips in cheats.items():
        if key >= 100:
            num_cheats += skips
    return num_cheats


def find_better_cheats(path: List[Tuple[int, int]]) -> Dict[int, int]:
    cheats: Dict[int, int] = Counter()
    path_idx_map = {p: len(path) - i - 1 for i, p in enumerate(path)}
    seen = set()
    for curr in path:
        # Check each direction
        row, col = curr
        curr_steps_to_end = path_idx_map[curr]
        seen.add(curr)
        for cand in path_idx_map:
            if cand in seen:  # should prevent backwards steps
                continue
            cand_row, cand_col = cand
            dist_away = abs(row - cand_row) + abs(col - cand_col)
            if dist_away > 20:
                continue
            steps_saved = curr_steps_to_end - path_idx_map[cand] - dist_away
            if steps_saved <= 20:
                continue
            cheats[steps_saved] += 1
    return cheats


def part2(_input: InputType) -> int:
    grid, start, end = _input
    path = walk(grid, start, end)
    cheats = find_better_cheats(path)
    print(sorted(cheats.items()))
    num_cheats = 0
    for key, skips in cheats.items():
        if key >= 100:
            num_cheats += skips
    return num_cheats


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
