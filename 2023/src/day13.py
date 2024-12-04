from typing import Any, Optional, List
import argparse

sample_file_path = "test/13.sample"
input_file_path = "test/13.input"


def check_symmetry(s: List[str], required_diffs: int = 0) -> (int, int):
    def check_symmetry_helper(s: List[str], idx: int) -> (bool, int):
        reflection_idx = idx + 1
        matching = 0
        total_diffs = 0
        while idx >= 0 and reflection_idx < len(s):
            left = s[idx]
            right = s[reflection_idx]
            curr_diffs = sum(0 if left[i] == right[i] else 1 for i in range(len(left)))
            total_diffs += curr_diffs
            if total_diffs <= required_diffs:
                matching += 1
            else:
                return False, matching
            idx -= 1
            reflection_idx += 1
        if total_diffs != required_diffs:
            return False, matching
        else:
            return True, matching

    best = 0
    best_idx = 0
    curr = 0
    for i in range(len(s) - 1):
        matching, curr = check_symmetry_helper(s, i)
        if matching:
            if curr > best:
                best = curr
                best_idx = i

    return best, best_idx


class Pattern13:
    orig: List[str]
    flipped: List[str]

    def __init__(self, pattern: List[str]):
        self.orig = pattern
        self.flipped = list(
            "".join(v) for v in zip(*[[c for c in row] for row in pattern])
        )


def parse_file_day13(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    patterns = []
    curr = []
    for line in lines:
        stripped = line.strip()
        if stripped == "":
            patterns.append(Pattern13(curr))
            curr = []
        else:
            curr.append(stripped.strip())
    else:
        patterns.append(Pattern13(curr))
    return patterns


def solve_day13_part1(input: List[Pattern13]) -> int:
    ans = 0
    for pattern in input:
        num_match_row, best_row = check_symmetry(pattern.orig)
        num_match_col, best_col = check_symmetry(pattern.flipped)
        if num_match_row > num_match_col:
            ans += (best_row + 1) * 100
        else:
            ans += best_col + 1
    return ans


def solve_day13_part2(input: List[Pattern13]) -> int:
    ans = 0
    for pattern in input:
        num_match_row, best_row = check_symmetry(pattern.orig, required_diffs=1)
        num_match_col, best_col = check_symmetry(pattern.flipped, required_diffs=1)
        if num_match_row > num_match_col:
            ans += (best_row + 1) * 100
        else:
            ans += best_col + 1
    return ans


def solve_day13(
    input: Any, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None
):
    out_part1 = solve_day13_part1(input)

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

    out_part2 = solve_day13_part2(input)
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


def main_13(run_all: bool = False, example: Optional[str] = None):
    if example:
        print("Testing input from cmd line")
        input = parse_file_day13("", example=example)
        solve_day13(input)
        exit(0)
    print("Running script for day 13")
    print("Sample input")
    expected_out_part1 = 405
    expected_out_part2 = 400
    print("---------------------------------")
    print("Input file:", sample_file_path)
    input = parse_file_day13(sample_file_path)
    solve_day13(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day13(input_file_path)
        solve_day13(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--actual", action="store_true")
    args = parser.parse_args()
    main_13(run_all=args.actual)
