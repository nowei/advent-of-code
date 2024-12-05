from typing import List, Tuple
from collections import Counter

parent_path = "src/days/day01/"


def _parse_input(sample: bool) -> Tuple[List[int], List[int]]:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    first = []
    second = []
    with open(file_name, "r") as f:
        for line in f:
            a, b = line.strip().split()
            first.append(int(a))
            second.append(int(b))
    return first, second


def part1(_input: Tuple[List[int], List[int]]) -> int:
    # Sort and get aligned diff
    first, second = _input
    sorted_first = sorted(first)
    sorted_second = sorted(second)
    diff = 0
    for i in range(len(sorted_first)):
        diff += abs(sorted_first[i] - sorted_second[i])
    return diff


def part2(_input: Tuple[List[int], List[int]]) -> int:
    # Process left list in order, count instances in second list
    first, second = _input
    counts_second = Counter(second)
    diff = 0
    for key in first:
        curr = key * counts_second.get(key, 0)
        diff += curr
    return diff


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
