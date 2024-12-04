from typing import Any, Optional, List, Dict
from collections import defaultdict, OrderedDict
import argparse

sample_file_path = "test/15.sample"
input_file_path = "test/15.input"


class Step15:
    value: str
    label: str
    focal: Optional[int]

    def __init__(self, value):
        self.value = value
        self.focal = None
        if "-" in self.value:
            self.label = value.strip("-")
        elif "=" in self.value:
            self.label, focal_str = value.split("=")
            self.focal = int(focal_str)

    def __hash__(self) -> int:
        val = 0
        for c in self.value:
            val += ord(c)
            val *= 17
            val %= 256
        return val

    def hash_label(self) -> int:
        val = 0
        for c in self.label:
            val += ord(c)
            val *= 17
            val %= 256
        return val


class Steps15:
    values: List[Step15]

    def __init__(self, values):
        self.values = values


def parse_file_day15(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    values = [Step15(v) for v in lines[0].strip().split(",")]
    return Steps15(values)


def solve_day15_part1(input: Steps15) -> int:
    val = 0
    for v in input.values:
        val += hash(v)
    return val


def solve_day15_part2(input: Steps15) -> int:
    boxes: Dict[int, Dict[str, int]] = defaultdict(lambda: OrderedDict())
    for v in input.values:
        box_num = v.hash_label()
        if v.focal is None:  # -
            if v.label in boxes[box_num]:
                boxes[box_num].pop(v.label)
        else:  # =
            boxes[box_num][v.label] = v.focal
    focusing = 0
    for box_num in boxes:
        for i, (values, focal) in enumerate(boxes[box_num].items()):
            focusing += (box_num + 1) * focal * (i + 1)
    return focusing


def solve_day15(
    input: Any, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None
):
    out_part1 = solve_day15_part1(input)

    if expected_pt1 is not None:
        if out_part1 != expected_pt1:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_pt1)
        else:
            print("Sample matched")
    print("Part 1 result:")
    print(out_part1)
    print()

    out_part2 = solve_day15_part2(input)
    if expected_pt2 is not None:
        if out_part2 != expected_pt2:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_pt2)
        else:
            print("Sample matched")
    print("Part 2 result:")
    print(out_part2)
    print()


def main_15(run_all: bool = False, example: Optional[str] = None):
    if example:
        print("Testing input from cmd line")
        input = parse_file_day15("", example=example)
        solve_day15(input)
        exit(0)

    print("Running script for day 15")
    print("Sample input")
    print("---------------------------------")
    expected_out_part1 = 1320
    expected_out_part2 = 145
    print("Input file:", sample_file_path)
    input = parse_file_day15(sample_file_path)
    solve_day15(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day15(input_file_path)
        solve_day15(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--actual", action="store_true")
    args = parser.parse_args()
    main_15(run_all=args.actual)
