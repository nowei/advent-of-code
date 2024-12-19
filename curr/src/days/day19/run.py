from typing import List, Tuple
from collections import deque


class Towels:
    available_towels: List[str]
    desired_designs: List[str]

    def __init__(self, available, desired):
        self.available_towels = available
        self.desired_designs = desired


InputType = Towels
parent_path = "src/days/day19/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"

    with open(file_name, "r") as f:
        available = f.readline().strip().split(", ")
        desired = []
        f.readline()
        for line in f:
            desired.append(line.strip())
    return Towels(available, desired)


def create(target: str, cands: List[str]):
    queue: deque[Tuple[int, str, int]] = deque()
    for c in cands:
        if c == target[0 : len(c)]:
            queue.append((1, c, len(c)))
    while queue:
        level, c, idx = queue.pop()
        if idx == len(target):
            return True
        if idx > len(target):
            continue
        for next_cand in cands:
            if next_cand == target[idx : idx + len(next_cand)]:
                queue.append((level + 1, next_cand, idx + len(next_cand)))
    return False


def part1(_input: InputType) -> int:
    towels = _input
    # Maybe a trie of some sort
    total = 0
    for i, t in enumerate(towels.desired_designs):
        total += create(t, towels.available_towels)
        print(i, t)
    return total


def create_dp(target: str, cands: List[str]):
    dp = [0] * (len(target) + 1)
    dp[0] = 1
    for i in range(len(dp)):
        if dp[i]:
            for c in cands:
                if c == target[i : i + len(c)]:
                    dp[i + len(c)] += dp[i]
    print(dp)
    return dp[-1]


# 54961 Too low
def part2(_input: InputType) -> int:
    towels = _input
    # Maybe a trie of some sort
    total = 0
    for i, t in enumerate(towels.desired_designs):
        total += create_dp(t, towels.available_towels)
        print(i, t)
    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
