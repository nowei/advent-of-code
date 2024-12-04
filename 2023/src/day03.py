from typing import Any, List, Tuple, Set
import argparse

sample_file_path = "test/03.sample"
input_file_path = "test/03.input"
expected_out_part1 = 4361
expected_out_part2 = 467835


def parse_file_day03(file_path) -> List[List[str]]:
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            lines.append([c for c in line.strip()])
    return lines


def check_valid_part(input: List[List[str]], digits_set: Set[Tuple[int, int]]) -> bool:
    width = len(input[0])
    height = len(input)
    for curr_row, curr_col in digits_set:
        for i in range(-1, 2):
            for j in range(-1, 2):
                check_row = curr_row + i
                check_col = curr_col + j
                if check_row < 0 or check_row >= height:
                    continue
                if check_col < 0 or check_col >= width:
                    continue
                if (check_row, check_col) in digits_set:
                    continue
                val = input[check_row][check_col]
                if not val.isdigit() and val != ".":
                    return True
    return False


def check_next_digits(
    input: List[List[str]], check_digit: Tuple[int, int], seen: Set[Tuple[int, int]]
) -> (bool, int):
    row, col = check_digit
    if not input[row][col].isdigit():
        return False, 0
    width = len(input[0])
    col_max = col
    while col_max < width and input[row][col_max].isdigit():
        col_max += 1
    digits_set = set((row, c) for c in range(col, col_max))
    for tup in digits_set:
        seen.add(tup)
    valid = check_valid_part(input, digits_set)
    val = 0
    if valid:
        for c in range(col, col_max):
            val = val * 10 + int(input[row][c])
    return valid, val


def solve_day03_part1(input: List[List[str]]) -> Any:
    seen = set()
    ans = 0
    # for each row
    for i in range(len(input)):
        # for each col
        for j in range(len(input[0])):
            if (i, j) in seen:
                continue
            # Note that we will always see the beginning of the digit since
            # we go from left to right, so we only need to check the remaining
            # digits, add it to seen, and check the surrounding values
            valid, part_number = check_next_digits(input, (i, j), seen)
            if valid:
                ans += part_number
            seen.add((i, j))
    return ans


def get_left_right_number(input: List[List[str]], check_digit: Tuple[int, int]) -> int:
    width = len(input[0])
    row, col = check_digit
    left_col, right_col = col, col
    while left_col >= 0 and input[row][left_col].isdigit():
        left_col -= 1
    while right_col < width and input[row][right_col].isdigit():
        right_col += 1

    val = 0
    for c in range(left_col + 1, right_col):
        val = val * 10 + int(input[row][c])
    return val


def check_surrounding_for_nums(
    input: List[List[str]], check_digit: Tuple[int, int]
) -> int:
    width = len(input[0])
    height = len(input)
    curr_row, curr_col = check_digit
    seen_numbers = 0
    seen_numbers_coords = set()
    # Note that if we do not see exactly 2 numbers adjacent to the *, we will skip and return 0
    # v.v
    # v*v
    # vvv
    # This means we care about contiguous rows of numbers, e.g. the above has 5 contiguous values
    # so we should reject this
    for i in range(-1, 2):
        contiguous = False
        for j in range(-1, 2):
            check_row = curr_row + i
            check_col = curr_col + j
            if check_row < 0 or check_row >= height:
                continue
            if check_col < 0 or check_col >= width:
                continue
            val = input[check_row][check_col]
            if val.isdigit():
                if not contiguous:
                    contiguous = True
                    seen_numbers += 1
                    seen_numbers_coords.add((check_row, check_col))
            else:
                contiguous = False
    if seen_numbers != 2:
        return 0
    val = 1
    for i, j in seen_numbers_coords:
        val *= get_left_right_number(input, (i, j))
    return val


def solve_day03_part2(input: List[List[str]]) -> Any:
    ans = 0
    # Look for gears (*)
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == "*":
                gear_ratio = check_surrounding_for_nums(input, (i, j))
                ans += gear_ratio
    return ans


def solve_day03(file_path: str, check_out: bool):
    input = parse_file_day03(file_path)
    out_part1 = solve_day03_part1(input)

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

    out_part2 = solve_day03_part2(input)
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


def main_03(run_all: bool = False):
    print("Running script for day 03")
    print("Sample input")
    solve_day03(sample_file_path, check_out=True)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day03(input_file_path, check_out=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--actual", action="store_true")
    args = parser.parse_args()
    main_03(run_all=args.actual)
