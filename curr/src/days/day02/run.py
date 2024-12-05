from typing import List

parent_path = "src/days/day02/"
InputType = List[List[int]]


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    lines = []
    with open(file_name, "r") as f:
        for line in f:
            lines.append([int(v) for v in line.strip().split()])
    return lines


def _is_safe(cand: List[int]) -> bool:
    prev = cand[0]
    direction = cand[0] < cand[1]
    for i in range(1, len(cand)):
        curr = cand[i]
        if curr == prev or abs(curr - prev) > 3:
            return False
        if direction:
            if prev > curr:
                return False
        else:
            if prev < curr:
                return False
        prev = curr
    return True


def part1(_input: InputType) -> int:
    num_safe = 0
    for cand in _input:
        if _is_safe(cand):
            num_safe += 1
    return num_safe


def _is_safe_tolerance(cand: List[int], max_tol: int = 1):
    curr_issues = 0
    # make array of consecutive differences
    diffs = []
    prev = cand[0]
    for curr in cand[1:]:
        diffs.append(curr - prev)
        prev = curr
    pos_cnt = 0
    neg_cnt = 0
    for diff in diffs:
        if diff > 0:
            pos_cnt += 1
        else:
            neg_cnt += 1

    # If all are positive or negative, we only need to check the
    if pos_cnt == 0 or neg_cnt == 0:
        if max(abs(d) for d in diffs) <= 3:
            return True
        else:
            return False

    if curr_issues > max_tol:
        return False
    return True


def part2(_input: InputType) -> int:
    num_safe = 0
    # Easiest solution would just be to brute force remove one item from the list and check if it still matches
    # Although you can technically code some smarter checks, e.g.
    # Determine trend if positive or negative, if > 1 peaks/valleys, then we know that we can't move
    # everything over and must return not safe. If no peaks and valleys (all in one direction), we only need to check that
    # the consecutive items do not differ by too much. If we see an item differ by too much, count it and
    # if the count of these things > the maximum tolerance, we know that there is no resolution.
    for cand in _input:
        for i in range(0, len(cand)):
            curr = cand[:i] + cand[i + 1 :]
            if _is_safe(curr):
                num_safe += 1
                break
    return num_safe


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
