from typing import Tuple, List

InputType = Tuple[List[List[int]], List[int]]
parent_path = "src/days/day05/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    fresh_ingredient_ranges = []
    ingredients = []
    with open(file_name, "r") as f:
        for line in f:
            if not line.strip():
                continue
            if "-" in line:
                fresh_ingredient_ranges.append(
                    [int(v.strip()) for v in line.split("-")]
                )
            else:
                ingredients.append(int(line.strip()))
    return fresh_ingredient_ranges, ingredients


def part1(_input: InputType) -> int:
    fresh_ingredient_ranges, ingredients = _input
    fresh_ingredient_ranges.sort()
    # merge ranges
    new_ranges = [fresh_ingredient_ranges[0]]
    for r in fresh_ingredient_ranges[1:]:
        # check within previous range
        if new_ranges[-1][0] <= r[0] <= new_ranges[-1][1]:
            if r[1] > new_ranges[-1][1]:
                new_ranges[-1][1] = r[1]
        else:
            new_ranges.append(r)
    fresh_ingredient_ranges = new_ranges
    valid = 0
    for ing in ingredients:
        for r in fresh_ingredient_ranges:
            if r[0] <= ing <= r[1]:
                valid += 1
                break

    return valid


def part2(_input: InputType) -> int:
    fresh_ingredient_ranges, ingredients = _input
    fresh_ingredient_ranges.sort()
    # merge ranges
    new_ranges = [fresh_ingredient_ranges[0]]
    for r in fresh_ingredient_ranges[1:]:
        # check within previous range
        print(r, new_ranges[-1])
        if new_ranges[-1][0] <= r[0] <= new_ranges[-1][1]:
            if r[1] > new_ranges[-1][1]:
                new_ranges[-1][1] = r[1]
        else:
            new_ranges.append(r)
    total = 0
    for r in new_ranges:
        print(r)
        total += r[1] - r[0] + 1
    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
