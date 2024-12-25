from typing import List, Tuple, Set

InputType = Tuple[List[List[str]], Tuple[int, int]]
parent_path = "src/days/day06/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    m = []
    with open(file_name, "r") as f:
        for line in f:
            m.append(list(line.strip()))
    pos = None
    for row in range(len(m)):
        for col in range(len(m[0])):
            if m[row][col] == "^":
                pos = (row, col)
                break
            if pos:
                break
    return m, pos or (0, 0)


dir_mapping = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}


def step(grid, row, col, direction) -> Tuple[int, int, Tuple[int, int]]:
    row_delta, col_delta = direction
    new_row = row + row_delta
    new_col = col + col_delta
    if (
        new_row >= 0
        and new_row < len(grid)
        and new_col >= 0
        and new_col < len(grid[0])
        and grid[new_row][new_col] == "#"
    ):
        direction = dir_mapping[direction]
    else:
        row = new_row
        col = new_col
    return row, col, direction


def _walk_pt1(
    grid: List[List[str]], starting_pos: Tuple[int, int]
) -> Tuple[Set[Tuple[int, int]], List[Tuple[int, int, Tuple[int, int]]]]:
    seen = set()
    path = []
    row, col = starting_pos
    # Row, col

    direction = (-1, 0)
    while row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]):
        seen.add((row, col))
        path.append((row, col, direction))
        row, col, direction = step(grid, row, col, direction)
    return seen, path


def part1(_input: InputType) -> int:
    grid, starting_pos = _input
    seen_squares = _walk_pt1(grid, starting_pos)[0]
    return len(seen_squares)


def _intersects_with_self(
    grid: List[List[str]],
    row: int,
    col: int,
    direction: Tuple[int, int],
    seen: Set[Tuple[int, int, Tuple[int, int]]],
) -> bool:
    while row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]):
        if (row, col, direction) in seen:
            return True
        seen.add((row, col, direction))
        row, col, direction = step(grid, row, col, direction)
    return False


# 2094 too high
# 2045 too high
# 1892 is not the right answer
def _replay_path_loop_count(
    grid: List[List[str]], path: List[Tuple[int, int, Tuple[int, int]]]
) -> int:
    seen: Set[Tuple[int, int, Tuple[int, int]]] = set()
    seen_coords: Set[Tuple[int, int]] = set()
    loop_possibilities = set()
    for p in path:
        seen.add(p)
        seen_coords.add(p[0:2])
        row, col, direction = p
        cand_row, cand_col, cand_direction = step(grid, row, col, direction)
        # There's already a rock there
        if direction != cand_direction:
            continue
        # If it's out of bounds, we can't consider it a candidate
        if (
            cand_row < 0
            or cand_row >= len(grid)
            or cand_col < 0
            or cand_col >= len(grid[0])
        ):
            continue
        # The candidate coordinate cannot be on the path we have already seen so far...
        if (cand_row, cand_col) in seen_coords:
            continue
        grid[cand_row][cand_col] = "#"
        if _intersects_with_self(grid, row, col, dir_mapping[direction], set(seen)):
            # Note that the loop possibilities are where we potentially place the stone, not the
            # point in which we will hit the stone
            loop_possibilities.add((cand_row, cand_col))
        grid[cand_row][cand_col] = "."
    return len(loop_possibilities)


def part2(_input: InputType) -> int:
    grid, starting_pos = _input
    _seen_squares, path = _walk_pt1(grid, starting_pos)
    count = _replay_path_loop_count(grid, path)
    return count


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
