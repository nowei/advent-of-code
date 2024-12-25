import re
from typing import Iterable

InputType = str
parent_path = "src/days/day03/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    with open(file_name, "r") as f:
        output = f.read()
    return output


def part1(_input: InputType) -> int:
    # Look for mul(x,y)
    muls: Iterable[str] = re.findall("mul\\(\\d{1,3},\\d{1,3}\\)", _input)
    total = 0
    for entry in muls:
        a, b = entry.replace("mul(", "").replace(")", "").split(",")
        total += int(a) * int(b)
    return total


def part2(_input: InputType) -> int:
    ops: Iterable[str] = re.findall(
        "(mul\\(\\d{1,3},\\d{1,3}\\)|do\\(\\)|don\\'t\\(\\))", _input
    )
    total = 0
    do = True
    for entry in ops:
        print(entry)
        if entry == "do()":
            do = True
        elif entry == "don't()":
            do = False
        else:
            if do:
                a, b = entry.replace("mul(", "").replace(")", "").split(",")
                total += int(a) * int(b)

    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
