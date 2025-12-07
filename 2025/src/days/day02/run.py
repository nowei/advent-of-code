from typing import List

InputType = List[List[int]]
parent_path = "src/days/day02/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"

    with open(file_name, "r") as f:
        ranges = [
            [int(v) for v in section.split("-")]
            for section in f.readline().strip().split(",")
        ]

    return ranges


def part1(_input: InputType) -> int:
    invalids = 0
    for left, right in _input:
        for val in range(left, right + 1):
            s_val = str(val)
            half = len(s_val) // 2
            if s_val.count(s_val[:half]) * half == len(s_val) and len(s_val) % 2 == 0:
                print(val, s_val[:half], half, len(s_val))
                invalids += val
    return invalids


def part2(_input: InputType) -> int:
    invalids = 0
    for left, right in _input:
        for val in range(left, right + 1):
            s_val = str(val)
            for i in range(1, len(s_val) // 2 + 1):
                if s_val.count(s_val[:i]) * i == len(s_val):
                    invalids += val
                    print(val)
                    break
    return invalids


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
