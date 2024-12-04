from typing import Any, List
import argparse

sample_file_path = "test/06.sample"
input_file_path = "test/06.input"
expected_out_part1 = 288
expected_out_part2 = 71503


class Setting_06:
    times: List[int]
    distances: List[int]

    def __init__(self, times: List[int], distances: List[int]) -> None:
        self.times = times
        self.distances = distances


def parse_file_day06(file_path) -> Any:
    with open(file_path, "r") as f:
        times = [int(v) for v in f.readline().split(":")[1].strip().split()]
        distances = [int(v) for v in f.readline().split(":")[1].strip().split()]
        setting = Setting_06(times, distances)
    return setting


# (t - x) * x = t*x - x*x
# derivative is
# t - x, this is 0 when t = x
def compute_pt1(time, held_time):
    return (time - held_time) * held_time


# Return the first index in which
def bin_search_lte(time, time_min, time_max, distance):
    left = time_min
    right = time_max

    while left < right:
        half = (left + right) // 2
        half_dist = compute_pt1(time, half)
        if half_dist > distance:
            right = half
        else:
            left = half + 1
    return right


def bin_search_gt(time, time_min, time_max, distance):
    left = time_min
    right = time_max

    while left < right:
        half = (left + right) // 2
        half_dist = compute_pt1(time, half)
        if half_dist > distance:
            left = half + 1
        else:
            right = half
    return left


def solve_day06_part1(input: Setting_06) -> int:
    ans = 1
    for i in range(len(input.times)):
        time = input.times[i]
        best_distance = input.distances[i]
        halfway = time // 2
        start_idx = bin_search_lte(time, 0, halfway, best_distance)
        end_idx = bin_search_gt(time, halfway, time, best_distance)
        ans *= end_idx - start_idx
    return ans


def solve_day06_part2(input: Setting_06) -> int:
    correct_kerning_time = int("".join([str(v) for v in input.times]))
    correct_kerning_distance = int("".join([str(v) for v in input.distances]))
    time = correct_kerning_time
    best_distance = correct_kerning_distance
    halfway = time // 2
    start_idx = bin_search_lte(time, 0, halfway, best_distance)
    end_idx = bin_search_gt(time, halfway, time, best_distance)
    return end_idx - start_idx


def solve_day06(file_path: str, check_out: bool):
    input = parse_file_day06(file_path)
    out_part1 = solve_day06_part1(input)

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

    out_part2 = solve_day06_part2(input)
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


def main_06(run_all: bool = False):
    print("Running script for day 06")
    print("Sample input")
    solve_day06(sample_file_path, check_out=True)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day06(input_file_path, check_out=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--actual", action="store_true")
    args = parser.parse_args()
    main_06(run_all=args.actual)
