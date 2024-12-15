from typing import Tuple, List, Dict
from collections import Counter


class Robot:
    position: Tuple[int, int]
    velocity: Tuple[int, int]
    grid: Tuple[int, int]

    def __init__(self, position, velocity, grid):
        self.position = position
        self.velocity = velocity
        self.grid = grid

    def walk(self, steps: int) -> Tuple[int, int]:
        row, col = self.position
        delta_row, delta_col = self.velocity
        curr_row = row + delta_row * steps
        curr_col = col + delta_col * steps
        final_row = curr_row % self.grid[0]
        final_col = curr_col % self.grid[1]
        return final_row, final_col


InputType = Tuple[Tuple[int, int], List[Robot]]
parent_path = "src/days/day14/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    grid = (7, 11) if sample else (103, 101)
    robots = []
    with open(file_name, "r") as f:
        for line in f:
            p_str, v_str = line.strip().split()
            pos = tuple([int(v) for v in p_str.split("=")[1].split(",")])[::-1]
            vel = tuple([int(v) for v in v_str.split("=")[1].split(",")])[::-1]
            robots.append(Robot(pos, vel, grid))
    return grid, robots


def visualize(grid: Tuple[int, int], positions: Dict[Tuple[int, int], int]):
    print("=============================================")
    for row in range(grid[0]):
        print(
            "".join(
                [
                    str(positions[(row, col)]) if (row, col) in positions else "."
                    for col in range(grid[1])
                ]
            )
        )


def compute_safety(grid: Tuple[int, int], positions: Dict[Tuple[int, int], int]):
    row_half = grid[0] // 2
    col_half = grid[1] // 2
    a, b, c, d = 0, 0, 0, 0
    for pos, value in positions.items():
        row, col = pos
        if row < row_half:
            if col < col_half:
                a += value
            elif col > col_half:
                b += value
        elif row > row_half:
            if col < col_half:
                c += value
            elif col > col_half:
                d += value
    return a * b * c * d


def part1(_input: InputType) -> int:
    grid, robots = _input
    steps = 100
    visualize(grid, Counter([r.position for r in robots]))
    final_positions: Dict[Tuple[int, int], int] = Counter()
    for robot in robots:
        final_positions[robot.walk(steps)] += 1
    visualize(grid, final_positions)
    safety_factor = compute_safety(grid, final_positions)
    return safety_factor


def part2(_input: InputType) -> int:
    grid, robots = _input
    visualize(grid, Counter([r.position for r in robots]))
    safety_factor = 0
    # tree - 7572
    for steps in range(98, 10000, 101):
        final_positions: Dict[Tuple[int, int], int] = Counter()
        for robot in robots:
            final_positions[robot.walk(steps)] += 1
        print(steps)
        visualize(grid, final_positions)

    # Horizontal grouping
    # for steps in range(156, 10000, 103):
    #     final_positions: Dict[Tuple[int, int], int] = Counter()
    #     for robot in robots:
    #         final_positions[robot.walk(steps)] += 1
    #     print(steps)
    #     visualize(grid, final_positions)
    # safety_factor = compute_safety(grid, final_positions)
    return safety_factor


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
