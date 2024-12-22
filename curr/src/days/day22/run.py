from typing import List

InputType = List[int]
parent_path = "src/days/day22/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        # file_name = parent_path + "sample.txt"
        file_name = parent_path + "sample2.txt"
    numbers = []
    with open(file_name, "r") as f:
        for line in f:
            numbers.append(int(line.strip()))
    return numbers


def _mix(sn, n):
    return sn ^ n


def _prune(sn):
    return sn % 16777216


def evolve(sn):
    sn = _prune(_mix(sn, sn * 64))
    sn = _prune(_mix(sn, sn // 32))
    sn = _prune(_mix(sn, sn * 2048))
    return sn


def part1(_input: InputType) -> int:
    secret_numbers = _input
    total = 0
    for initial_secret_number in secret_numbers:
        sn = initial_secret_number
        for i in range(2000):
            sn = evolve(sn)
        total += sn
    return total


def part2(_input: InputType) -> int:
    secret_numbers = _input
    total = 0
    change_sequence_tracker = {}
    for initial_secret_number in secret_numbers:
        sn = initial_secret_number
        current_secret_numbers_modded = [initial_secret_number % 10]
        for _ in range(2000):
            sn = evolve(sn)
            current_secret_numbers_modded.append(sn % 10)
        change_list = []
        for i in range(1, len(current_secret_numbers_modded)):
            change_list.append(
                current_secret_numbers_modded[i] - current_secret_numbers_modded[i - 1]
            )
        current_change_sequence_tracker = {}
        # print(change_list)
        for i in range(3, len(change_list)):
            cand = tuple(change_list[i - 3 : i + 1])
            if cand in current_change_sequence_tracker:
                continue
            current_change_sequence_tracker[cand] = current_secret_numbers_modded[i + 1]
        # print(current_change_sequence_tracker)
        for cand in current_change_sequence_tracker:
            if cand not in change_sequence_tracker:
                change_sequence_tracker[cand] = 0
            change_sequence_tracker[cand] += current_change_sequence_tracker[cand]
    total = max(change_sequence_tracker.values())
    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
