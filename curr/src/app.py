# TODO: dynamic imports based on which day we're running
import importlib
import argparse

# import sys
import os


def _get_day_str(day_to_run: int):
    return str(day_to_run).zfill(2)


def _run(day_to_run: int, part: int, execute=True):
    module_name = f"days.day{_get_day_str(day_to_run)}.run"
    # TODO: Format by day
    mod = importlib.import_module(module_name)
    result = mod.exec(part, execute)
    if execute:
        print("actual result...")
    else:
        print("sample result...")
    print(result)


def _generate(day_to_run: int):
    day_str = _get_day_str(day_to_run)
    parent = f"src/days/day{day_str}/"
    if not os.path.isdir(parent):
        os.mkdir(parent)
    with open("src/days/day00/run.py", "r") as f:
        with open(parent + "run.py", "w") as g:
            g.write(f.read().format(day_str))
    with open(parent + "input.txt", "w") as f:
        pass
    with open(parent + "sample.txt", "w") as f:
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
    parser.add_argument(
        "--run-all",
        dest="run_all",
        help="run all",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--part",
        dest="part",
        help="which part to run",
        type=int,
        default=1,
    )
    args = parser.parse_args()
    generate = args.generate
    day = args.day
    execute = args.execute
    _run_all = args.run_all
    part = args.part

    if not day or (day < 1 or day > 25):
        print("please enter a day between [1, 25]")
        exit(1)
    if part <= 0 or part > 2:
        print("please enter a part between [1, 2]")
        exit(1)
    if generate:
        _generate(day)
    else:
        _run(day, part, execute)


if __name__ == "__main__":
    main()
