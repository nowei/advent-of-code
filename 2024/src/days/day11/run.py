from typing import Dict, List, Tuple
from collections import defaultdict

InputType = List[int]
parent_path = "src/days/day11/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    result = []
    with open(file_name, "r") as f:
        result = [int(v) for v in f.read().strip().split()]
    return result


def evaluate(stone: int):
    if stone == 0:
        return [1]
    s = str(stone)
    if len(s) % 2 == 0:
        half = len(s) // 2
        return [int(s[:half]), int(s[half:])]
    return [stone * 2024]


def _simulate(stones: List[int], steps: int) -> List[int]:
    curr = stones
    for i in range(steps):
        new_layer = []
        for stone in curr:
            new_layer.extend(evaluate(stone))
        if i < 10:
            print(stones, len(new_layer), new_layer)
        else:
            print(stones, len(new_layer))
        curr = new_layer
    return curr


def part1(_input: InputType) -> int:
    result = _simulate(_input, 25)
    return len(result)


# 9 17 15 43 40 70 126 153 317
def _memo(stones: List[int], steps: int) -> int:
    memo: Dict[Tuple[int, int], int] = {}

    def forward(stone: int, step: int):
        if step == 0:
            return 1
        if (stone, step) in memo:
            return memo[(stone, step)]
        curr = 0
        for new_stone in evaluate(stone):
            curr += forward(new_stone, step - 1)
        memo[(stone, step)] = curr
        return curr

    result = sum([forward(stone, steps) for stone in stones])
    return result


def _counter(stones: List[int], steps: int) -> int:
    counter: Dict[int, int] = defaultdict(lambda: 0)
    for stone in stones:
        counter[stone] += 1
    for _i in range(steps):
        new_counter: Dict[int, int] = defaultdict(lambda: 0)
        for stone, instances in counter.items():
            for new_stone in evaluate(stone):
                new_counter[new_stone] += instances
        counter = new_counter
        # print(_i, len(counter), sum(counter.values()))
        # print(max(counter), counter[max(counter)])
    return sum(counter.values())


def part2(_input: InputType) -> int:
    result = _memo(_input, 75)
    result2 = _counter(_input, 75)
    return max(result, result2)


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
