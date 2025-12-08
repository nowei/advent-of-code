from typing import List, Tuple

InputType = Tuple[List[List[str]], List[str]]
parent_path = "src/days/day06/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    lines = []
    orig_lines = []
    with open(file_name, "r") as f:
        for line in f:
            lines.append(line.strip().split())
            if line[-1] == "\n":
                line = line[:-1]
            orig_lines.append(line)
    return lines, orig_lines


def part1(_input: InputType) -> int:
    total = 0
    lines, orig_lines = _input
    for line in zip(*lines):
        print(line)
        operator = line[-1]
        val = 0
        if operator == "*":
            val = 1
        for v in line[:-1]:
            curr_val = int(v)
            if operator == "*":
                val *= curr_val
            else:
                val += curr_val
        total += val
    return total


def part2(_input: InputType) -> int:
    total = 0
    lines, orig_lines = _input
    equations: List[List[str]] = [[]]
    for col in range(len(orig_lines[0]) - 1, -1, -1):
        if all(orig_lines[i][col] == " " for i in range(len(orig_lines))):
            # new equation
            equations.append([])
            continue
        equations[-1].append(
            "".join([orig_lines[i][col] for i in range(len(orig_lines))])
        )
    for equation in equations:
        val = 0
        if "*" in equation[-1]:
            operator = "*"
            val = 1
        else:
            operator = "+"
        for line in equation:
            v = line.replace("*", "").replace("+", "").strip()
            if v.isdigit():
                if operator == "*":
                    val *= int(v)
                else:
                    val += int(v)
        total += val

    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
