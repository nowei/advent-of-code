from typing import List, Tuple, Dict, Set
from collections import defaultdict

InputType = Tuple[Dict[int, Set[int]], Dict[int, Set[int]], List[List[int]]]
parent_path = "src/days/day05/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    # x|y
    # map of x -> y
    # x is before y
    ordering_before = defaultdict(set)
    # y is after x
    ordering_after = defaultdict(set)
    manuals = []
    with open(file_name, "r") as f:
        for line in f:
            if "|" in line:
                before, after = line.strip().split("|")
                ordering_before[int(before)].add(int(after))
                ordering_after[int(after)].add(int(before))
            elif "," in line:
                manuals.append([int(v) for v in line.strip().split(",")])
    return ordering_before, ordering_after, manuals


def _check_inclusion(
    _cand: int,
    following: Set[int],
    preceding: Set[int],
    before: List[int],
    after: List[int],
) -> bool:
    result = None
    if not following and not preceding:
        result = True
    # if any of the before is in the following set, return False
    # if any of the after is in the preceding set, return False
    else:
        if any(b in following for b in before):
            result = False
        elif any(a in preceding for a in after):
            result = False
        else:
            result = True
    return result


def part1(_input: InputType) -> int:
    ordering_before, ordering_after, manuals = _input
    total = 0
    for manual in manuals:
        success = True
        for i in range(len(manual)):
            curr = manual[i]
            if not _check_inclusion(
                curr,
                ordering_before[curr],
                ordering_after[curr],
                manual[:i],
                manual[i + 1 :],
            ):
                success = False
                break
        if success:
            total += manual[len(manual) // 2]
    return total


def _correct_manual(
    ordering_before: Dict[int, Set[int]],
    ordering_after: Dict[int, Set[int]],
    manual: List[int],
) -> List[int]:
    # One thing we assume is that there's always a correct ordering
    manual = list(manual)
    reset_i = -1
    i = 0
    while i <= len(manual):
        if i == len(manual):
            if reset_i != -1:
                i = reset_i
                reset_i = -1
            else:
                break

        curr = manual[i]
        before = manual[:i]
        after = manual[i + 1 :]
        following = ordering_before[curr]
        preceding = ordering_after[curr]
        if _check_inclusion(
            curr,
            following,
            preceding,
            before,
            after,
        ):
            i += 1
            continue
        if reset_i == -1:
            reset_i = i
        # This can be faster if we just move it up to the last true thing or something.
        if before and [b in following for b in before][-1]:
            # print("before swapping", manual[i], manual[i - 1])
            manual[i], manual[i - 1] = manual[i - 1], manual[i]
        elif after and [a in preceding for a in after][0]:
            # print("after swapping", manual[i], manual[i + 1])
            manual[i], manual[i + 1] = manual[i + 1], manual[i]
        i += 1
    return manual


def part2(_input: InputType) -> int:
    ordering_before, ordering_after, manuals = _input
    total = 0
    for manual in manuals:
        success = True
        for i in range(len(manual)):
            curr = manual[i]
            if not _check_inclusion(
                curr,
                ordering_before[curr],
                ordering_after[curr],
                manual[:i],
                manual[i + 1 :],
            ):
                success = False
                break
        if not success:
            # Correct the ordering
            corrected_manual = _correct_manual(ordering_before, ordering_after, manual)
            print(manual, corrected_manual)
            total += corrected_manual[len(manual) // 2]
    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
