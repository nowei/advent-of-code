InputType = int
parent_path = "src/days/day{}/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"

    with open(file_name, "r") as f:
        for line in f:
            print(line)
    return 0


def part1(_input: InputType) -> int:
    return 0


def part2(_input: InputType) -> int:
    return 0


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
