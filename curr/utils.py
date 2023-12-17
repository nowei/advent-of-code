import argparse
import os.path

base_text = """from typing import Any, Optional, List, Tuple
import argparse

sample_file_path = "test/{day}.sample"
input_file_path = "test/{day}.input"

class Setting{day}:

    def __init__(self):
        pass

def parse_file_day{day}(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    for line in lines:
        line.strip()
    return None

def solve_day{day}_part1(input: Setting{day}) -> int:
    return 0

def solve_day{day}_part2(input: Setting{day}) -> int:
    return 0

def solve_day{day}(input: Setting{day}, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None):
    out_part1 = solve_day{day}_part1(input)

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

    out_part2 = solve_day{day}_part2(input)
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

def main_{day}(run_all: bool = False, example: Optional[str] = None):
    if example:
        print("Testing input from cmd line")
        input = parse_file_day{day}("", example=example)
        solve_day{day}(input)
        exit(0)

    print("Running script for day {day}")
    print("Sample input")
    print("---------------------------------")
    expected_out_part1 = None
    expected_out_part2 = None
    print("Input file:", sample_file_path)
    input = parse_file_day{day}(sample_file_path)
    solve_day{day}(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day{day}(input_file_path)
        solve_day{day}(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_{day}(run_all=args.actual)
"""

def generate_files(day: int):
    day_dict = {"day": "{:02d}".format(day)}
    if os.path.isfile("src/day{day}.py".format_map(day_dict)):
        v = input("are you sure? y/n\n")
        if v != "y":
            exit(1)
    with open("src/day{day}.py".format_map(day_dict), "w") as f:
        out = base_text.format_map(day_dict)
        f.write(out)
    # touch files to create them
    with open("test/{day}.sample".format_map(day_dict), "w") as f:
        pass
    with open("test/{day}.input".format_map(day_dict), "w") as f:
        pass

def main():
    parser = argparse.ArgumentParser(prog="generate template")
    parser.add_argument("-d", "--day")
    args = parser.parse_args()
    if not args.day:
        print("utils script requires a day argument")
        exit()
    generate_files(int(args.day))

if __name__ == '__main__':
    main()
