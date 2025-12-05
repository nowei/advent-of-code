from typing import List
import math

InputType = List[int]
parent_path = "src/days/day01/"


def get_sign(number):
    return math.copysign(1, number)


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"

    input_array = []
    with open(file_name, "r") as f:
        for line in f:
            direction = 1
            if "L" in line:
                direction = -1
            val = int(line.strip().strip("L").strip("R"))
            input_array.append(direction * val)
    return input_array


def part1(_input: InputType) -> int:
    curr_point = 50
    num_zeros = 0
    for turn in _input:
        curr_point += turn
        curr_point %= 100
        if curr_point == 0:
            num_zeros += 1
    return num_zeros


def part2(_input: InputType) -> int:
    curr_point = 50
    num_passed_zeros = 0
    for turn in _input:
        prev_point = curr_point
        curr_point += turn
        # Catch case when pointing at zero,
        if curr_point == 0 or (
            prev_point != 0 and get_sign(prev_point) != get_sign(curr_point)
        ):
            num_passed_zeros += 1
        num_passed_zeros += abs(curr_point) // 100
        print(prev_point, turn, curr_point, num_passed_zeros)
        curr_point %= 100
    return num_passed_zeros


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
