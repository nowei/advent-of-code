from typing import Any, Optional, List
import argparse

sample_file_path = "test/14.sample"
input_file_path = "test/14.input"


class Dish14:
    configuration: List[List[str]]

    def __init__(self, configuration) -> None:
        self.configuration = configuration

    # We can rotate counter-clockwise to move east to north and so forth until we have
    def shift_north(self) -> "Dish14":
        new_config = [
            ["." for _ in range(len(self.configuration[0]))]
            for _ in range(len(self.configuration))
        ]
        for col in range(len(self.configuration[0])):
            bottom = 0
            for row in range(len(self.configuration)):
                c = self.configuration[row][col]
                if c == "O":
                    new_config[bottom][col] = "O"
                    bottom += 1
                elif c == "#":
                    new_config[row][col] = "#"
                    bottom = row + 1

        return Dish14(new_config)

    # North -> West -> South -> East
    # This is rotating clockwise
    # top-left -> top-right
    # top-right -> bot-right
    # ^------------->|
    # |              |
    # |    rotate    |
    # |              |
    # <--------------v
    def rotate(self):
        res = [[] for _ in range(len(self.configuration[0]))]
        for col in range(len(self.configuration[0])):
            for row in range(len(self.configuration) - 1, -1, -1):
                res[col].append(self.configuration[row][col])
        return Dish14(res)

    def compute_load(self):
        total_height = len(self.configuration)
        load = 0
        for row in range(len(self.configuration)):
            for col in range(len(self.configuration[0])):
                if self.configuration[row][col] == "O":
                    load += total_height - row
        return load

    def __repr__(self) -> str:
        return str(self) + "\n"

    def __eq__(self, other):
        for i in range(len(self.configuration)):
            if self.configuration[i] == other.configuration[i]:
                return True
        return False

    def __str__(self):
        return "\n".join("".join(row) for row in self.configuration)

    def __hash__(self):
        return hash(str(self))


def parse_file_day14(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    config = []
    for line in lines:
        config.append(list(line.strip()))
    return Dish14(config)


def solve_day14_part1(input: Dish14) -> int:
    result = input.shift_north()
    return result.compute_load()


def solve_day14_part2(input: Dish14) -> int:
    curr = input
    # one cycle
    seen = {}
    cycle_ind = 0
    while curr not in seen:
        seen[curr] = cycle_ind
        curr = curr.shift_north()
        curr = curr.rotate().shift_north()
        curr = curr.rotate().shift_north()
        curr = curr.rotate().shift_north()
        curr = curr.rotate()
        cycle_ind += 1
    cycle_start = seen[curr]
    cycle_length = cycle_ind - cycle_start
    remaining = (1000000000 - cycle_start) % cycle_length
    for _ in range(remaining):
        curr = curr.shift_north()
        curr = curr.rotate().shift_north()
        curr = curr.rotate().shift_north()
        curr = curr.rotate().shift_north()
        curr = curr.rotate()

    return curr.compute_load()


def solve_day14(
    input: Any, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None
):
    out_part1 = solve_day14_part1(input)

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

    out_part2 = solve_day14_part2(input)
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


def main_14(run_all: bool = False, example: Optional[str] = None):
    if example:
        print("Testing input from cmd line")
        input = parse_file_day14("", example=example)
        solve_day14(input)
        exit(0)
    print("Running script for day 14")
    print("Sample input")
    expected_out_part1 = 136
    expected_out_part2 = 64
    print("---------------------------------")
    print("Input file:", sample_file_path)
    input = parse_file_day14(sample_file_path)
    solve_day14(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day14(input_file_path)
        solve_day14(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--actual", action="store_true")
    args = parser.parse_args()
    main_14(run_all=args.actual)
