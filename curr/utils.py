import argparse

base_text = """
from typing import Any
import argparse

sample_file_path = "test/{day}.sample"
input_file_path = "test/{day}.input"
expected_out_part1 = None
expected_out_part2 = None


def parse_file_day{day}(file_path) -> Any:
    with open(file_path, "r") as f:
        for line in f:
            pass

def solve_day{day}_part1(input: Any) -> Any:
    return None

def solve_day{day}_part2(input: Any) -> Any:
    return None

def solve_day{day}(file_path: str, check_out: bool):
    input = parse_file_day{day}(file_path)
    out_part1 = solve_day{day}_part1(input)

    if check_out:
        if out_part1 != expected_out_part1:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_out_part1)
        else:
            print("Sample matched")
    print("Part 1 result:")
    print(out_part1)
    print()

    out_part2 = solve_day{day}_part2(input)
    if check_out:
        if out_part2 != expected_out_part2:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_out_part2)
        else:
            print("Sample matched")
    print("Part 2 result:")
    print(out_part2)
    print()

def main_{day}(run_all: bool = False):
    print("Running script for day {day}")
    print("Sample input")
    solve_day{day}(sample_file_path, check_out=True)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day{day}(input_file_path, check_out=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_{day}(run_all=args.actual)
"""

def generate_files(day: int):
    day_dict = {"day": "{:02d}".format(day)}
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
