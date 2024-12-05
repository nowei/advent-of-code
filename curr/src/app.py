# TODO: dynamic imports based on which day we're running
import importlib
import argparse
# import sys
# import os

# # Get the current directory
# current_dir = os.getcwd()

# # Add the current directory to the path
# sys.path.append(current_dir)


def run(day_to_run: int, execute=True):
    module_name = f"days.day{str(day_to_run).zfill(2)}.run"
    # TODO: Format by day
    mod = importlib.import_module(module_name)
    result = mod.exec(execute)
    if execute:
        print("actual result...")
    else:
        print("sample result...")
    print(result)


def generate(day_to_run: int):
    pass


def main():
    parser = argparse.ArgumentParser("aoc2024")
    parser.add_argument("--day", dest="day", type=int, help="day of thing to run")
    parser.add_argument(
        "--generate",
        dest="generate",
        help="generate files",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--execute",
        dest="execute",
        help="run actual test case",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()
    generate = args.generate
    day = args.day
    execute = args.execute
    if generate:
        generate(day)
    else:
        if not day or (day < 1 or day > 25):
            print("please enter a day between [1, 25]")
        else:
            run(day, execute)


if __name__ == "__main__":
    main()
