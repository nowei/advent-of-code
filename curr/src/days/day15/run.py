from typing import List, Tuple

InputType = Tuple[List[List[str]], str]
parent_path = "src/days/day15/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
        # file_name = parent_path + "smaller.txt"
    grid = []
    directions = ""
    mapping = False
    with open(file_name, "r") as f:
        for line in f:
            if line == "\n":
                mapping = True
                continue
            if mapping:
                directions += line.strip()
            else:
                grid.append(list(line.strip()))
    return grid, directions


def _compute_gps(grid: List[List[str]]):
    total = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "O":
                total += row * 100 + col
    return total


def _get_position(grid: List[List[str]]) -> Tuple[int, int]:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "@":
                return row, col
    return 0, 0


directions_map = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def push(
    grid: List[List[str]],
    position: Tuple[int, int],
    directions: Tuple[int, int],
) -> Tuple[int, int]:
    # push all "O" characters in some direction by one unit
    pos_row, pos_col = position
    delta_row, delta_col = directions
    final_row, final_col = pos_row + delta_row, pos_col + delta_col
    new_row, new_col = final_row, final_col
    to_move = [(pos_row, pos_col)]
    while grid[new_row][new_col] == "O":
        to_move.append((new_row, new_col))
        new_row += delta_row
        new_col += delta_col
    if grid[new_row][new_col] == "#":
        # Do not do anything
        return pos_row, pos_col
    for move_row, move_col in to_move[::-1]:
        grid[move_row + delta_row][move_col + delta_col], grid[move_row][move_col] = (
            grid[move_row][move_col],
            grid[move_row + delta_row][move_col + delta_col],
        )
    return final_row, final_col


def _simulate(starting_grid: List[List[str]], directions: str):
    grid = [list(g) for g in starting_grid]
    pos_row, pos_col = _get_position(grid)
    for d in directions:
        delta_row, delta_col = directions_map[d]
        new_row = pos_row + delta_row
        new_col = pos_col + delta_col
        if grid[new_row][new_col] == ".":
            grid[new_row][new_col], grid[pos_row][pos_col] = "@", "."
            print(new_row, new_col, pos_row, pos_col)
            pos_row, pos_col = new_row, new_col
        elif grid[new_row][new_col] == "#":
            continue
        else:  # O
            pos_row, pos_col = push(grid, (pos_row, pos_col), directions_map[d])

    return grid


def _visualize(grid: List[List[str]]):
    for line in grid:
        print("".join(line))


def part1(_input: InputType) -> int:
    grid, directions = _input
    final_grid = _simulate(grid, directions)
    _visualize(final_grid)
    return _compute_gps(final_grid)


def _expand(old_grid: List[List[str]]):
    new_grid = []
    for line in old_grid:
        curr_line = []
        for c in line:
            if c == "#":
                curr_line.append("#")
                curr_line.append("#")
            elif c == "O":
                curr_line.append("[")
                curr_line.append("]")
            elif c == ".":
                curr_line.append(".")
                curr_line.append(".")
            elif c == "@":
                curr_line.append("@")
                curr_line.append(".")
        new_grid.append(curr_line)

    return new_grid


def push2_updown(
    grid: List[List[str]],
    position: Tuple[int, int],
    directions: Tuple[int, int],
):
    pos_row, pos_col = position
    delta_row, delta_col = directions
    final_row, final_col = pos_row + delta_row, pos_col + delta_col
    to_move_layers = [set([(pos_row, pos_col)])]
    some_boxes = True
    while some_boxes:
        new_layer = set()
        some_boxes = False
        for curr_row, curr_col in to_move_layers[-1]:
            try_row, try_col = curr_row + delta_row, curr_col + delta_col
            if grid[try_row][try_col] == "#":
                # Cannot move if anything above it is a #
                return pos_row, pos_col
            elif grid[try_row][try_col] == "]":
                new_layer.add((try_row, try_col))
                new_layer.add((try_row, try_col - 1))
                some_boxes = True
            elif grid[try_row][try_col] == "[":
                new_layer.add((try_row, try_col))
                new_layer.add((try_row, try_col + 1))
                some_boxes = True
        to_move_layers.append(new_layer)
    for layer in to_move_layers[::-1]:
        for move_row, move_col in layer:
            (
                grid[move_row + delta_row][move_col + delta_col],
                grid[move_row][move_col],
            ) = (
                grid[move_row][move_col],
                grid[move_row + delta_row][move_col + delta_col],
            )
    return final_row, final_col


def push2_leftright(
    grid: List[List[str]],
    position: Tuple[int, int],
    directions: Tuple[int, int],
):
    pos_row, pos_col = position
    delta_row, delta_col = directions
    final_row, final_col = pos_row + delta_row, pos_col + delta_col
    new_row, new_col = final_row, final_col
    to_move = [(pos_row, pos_col)]
    while grid[new_row][new_col] in "[]":
        to_move.append((new_row, new_col))
        to_move.append((new_row, new_col + delta_col))
        new_row += delta_row
        new_col += delta_col * 2
    if grid[new_row][new_col] == "#":
        return pos_row, pos_col
    for move_row, move_col in to_move[::-1]:
        grid[move_row + delta_row][move_col + delta_col], grid[move_row][move_col] = (
            grid[move_row][move_col],
            grid[move_row + delta_row][move_col + delta_col],
        )
    return final_row, final_col


def push2(
    grid: List[List[str]],
    position: Tuple[int, int],
    directions: Tuple[int, int],
) -> Tuple[int, int]:
    # push all "[]" characters in some direction by one unit
    if abs(directions[0]):
        return push2_updown(grid, position, directions)
    else:
        return push2_leftright(grid, position, directions)


def _simulate2(starting_grid: List[List[str]], directions: str):
    grid = [list(g) for g in starting_grid]
    pos_row, pos_col = _get_position(grid)
    for i, d in enumerate(directions):
        delta_row, delta_col = directions_map[d]
        new_row = pos_row + delta_row
        new_col = pos_col + delta_col
        if grid[new_row][new_col] == ".":
            grid[new_row][new_col], grid[pos_row][pos_col] = "@", "."
            pos_row, pos_col = new_row, new_col
        elif grid[new_row][new_col] == "#":
            continue
        else:  # [ or ] characters
            pos_row, pos_col = push2(grid, (pos_row, pos_col), directions_map[d])

    return grid


def _compute_gps2(grid: List[List[str]]):
    total = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "[":
                total += row * 100 + col
    return total


def part2(_input: InputType) -> int:
    old_grid, directions = _input
    grid = _expand(old_grid)
    _visualize(grid)
    final_grid = _simulate2(grid, directions)
    _visualize(final_grid)
    return _compute_gps2(final_grid)


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
