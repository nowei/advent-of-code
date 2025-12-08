from typing import List

InputType = List[str]
parent_path = "src/days/day04/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    graph = []
    with open(file_name, "r") as f:
        for line in f:
            graph.append(line.strip())
    return graph


def part1(_input: InputType) -> int:
    total_accessible_rolls = 0
    for i in range(len(_input)):
        for j in range(len(_input[0])):
            if _input[i][j] != "@":
                continue
            num_rolls = 0
            for d_i in range(-1, 2):
                for d_j in range(-1, 2):
                    if d_i == 0 and d_j == 0:
                        continue
                    if i + d_i < 0 or i + d_i >= len(_input):
                        continue
                    if j + d_j < 0 or j + d_j >= len(_input[0]):
                        continue
                    if _input[i + d_i][j + d_j] == "@":
                        num_rolls += 1
            if num_rolls < 4:
                total_accessible_rolls += 1
    return total_accessible_rolls


def part2(_input: InputType) -> int:
    rolls_removed = True
    total_rolls_removed = 0
    _input = [list(s) for s in _input]
    while rolls_removed:
        rolls_removed = False
        changing_rolls = []
        for i in range(len(_input)):
            for j in range(len(_input[0])):
                if _input[i][j] != "@":
                    continue
                num_rolls = 0
                for d_i in range(-1, 2):
                    for d_j in range(-1, 2):
                        if d_i == 0 and d_j == 0:
                            continue
                        if i + d_i < 0 or i + d_i >= len(_input):
                            continue
                        if j + d_j < 0 or j + d_j >= len(_input[0]):
                            continue
                        if _input[i + d_i][j + d_j] == "@":
                            num_rolls += 1
                if num_rolls < 4:
                    changing_rolls.append((i, j))
        total_rolls_removed += len(changing_rolls)
        for i, j in changing_rolls:
            _input[i][j] = "."
        if changing_rolls:
            rolls_removed = True

    return total_rolls_removed


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
