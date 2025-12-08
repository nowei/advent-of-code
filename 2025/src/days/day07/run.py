from typing import List

InputType = List[List[str]]
parent_path = "src/days/day07/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    mapping = []
    with open(file_name, "r") as f:
        for line in f:
            mapping.append(list(line.strip()))
    return mapping


def part1(_input: InputType) -> int:
    # copy mapping
    mapping = [list(line) for line in _input]
    splits = 0
    for i in range(1, len(mapping)):
        for j in range(len(mapping[0])):
            if mapping[i - 1][j] in ["|", "S"]:
                if mapping[i][j] == "^":
                    mapping[i][j - 1] = "|"
                    mapping[i][j + 1] = "|"
                    splits += 1
                else:
                    mapping[i][j] = "|"
    return splits


def part2(_input: InputType) -> int:
    mapping = [list(line) for line in _input]
    splits = 0
    futures = [0 for _ in range(len(mapping[0]))]
    for i in range(1, len(mapping)):
        next_futures = [0 for _ in range(len(mapping[0]))]
        for j in range(len(mapping[0])):
            if mapping[i - 1][j] in ["|", "S"]:
                if mapping[i][j] == "^":
                    mapping[i][j - 1] = "|"
                    mapping[i][j + 1] = "|"
                    splits += 1
                    next_futures[j + 1] += futures[j]
                    next_futures[j - 1] += futures[j]
                else:
                    mapping[i][j] = "|"
                    next_futures[j] += futures[j]
                    if mapping[i - 1][j] == "S":
                        next_futures[j] = 1
        futures = next_futures
    return sum(futures)


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
