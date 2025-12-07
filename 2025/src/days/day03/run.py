from typing import List

InputType = List[List[int]]
parent_path = "src/days/day03/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    entries = []
    with open(file_name, "r") as f:
        for line in f:
            entries.append([int(v) for v in line.strip()])
    return entries


def part1(_input: InputType) -> int:
    total = 0
    for entry in _input:
        best_val = 0
        cand_top = 0
        cand_bot = 0
        # Check two numbers for candidate best numbers
        for curr_val in entry:
            if not cand_top:
                cand_top = curr_val
            elif curr_val > cand_top:
                if cand_top * 10 + curr_val > best_val:
                    best_val = cand_top * 10 + curr_val
                cand_top = curr_val
                cand_bot = 0
            elif curr_val > cand_bot:
                cand_bot = curr_val
            elif not cand_bot:
                cand_bot = curr_val
            if cand_top and cand_bot:
                if cand_top * 10 + cand_bot > best_val:
                    best_val = cand_top * 10 + cand_bot
        total += best_val
    return total


def part2(_input: InputType) -> int:
    total = 0
    # Candidate starts as right 12 characters
    for entry in _input:
        cand = entry[-12:]
        new_min = 0
        new_max = len(entry) - 12
        for i in range(len(cand)):
            # For each candidate (from the left), move
            # the candidate to the left if the number
            # is greater or equal to it because it is a
            # bigger number or gives more options to
            # the other candidate slots.
            for j in range(new_max, new_min - 1, -1):
                if entry[j] >= cand[i]:
                    cand[i] = entry[j]
                    new_min = j + 1
            new_max += 1
        total += int("".join([str(v) for v in cand]))
    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
