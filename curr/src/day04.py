from typing import Any, List, Set
import argparse

sample_file_path = "test/04.sample"
input_file_path = "test/04.input"
expected_out_part1 = 13
expected_out_part2 = 30

class CardGame04:
    id: int
    winning_nums: Set[int]
    actual_nums: List[int]

    def __init__(self, id, winning_nums, actual_nums):
        self.id = id
        self.winning_nums = set(winning_nums)
        self.actual_nums = actual_nums

    def points(self) -> int:
        seen = 0
        for v in self.actual_nums:
            if v in self.winning_nums:
                seen += 1
        if seen == 0:
            return 0
        return 2 ** (seen - 1)
    def matches(self) -> int:
        seen = 0
        for v in self.actual_nums:
            if v in self.winning_nums:
                seen += 1
        return seen

def parse_file_day04(file_path) -> List[CardGame04]:
    games = []
    with open(file_path, "r") as f:
        for line in f:
            card_id_str, winning_numbers = line.split(":")
            _, id_str = card_id_str.split()
            winning_strs, actual_strs = winning_numbers.split("|")
            winning = [int(v) for v in winning_strs.split()]
            actual = [int(v) for v in actual_strs.split()]
            game = CardGame04(int(id_str), winning, actual)
            games.append(game)
    return games


def solve_day04_part1(input: List[CardGame04]) -> Any:
    ans = 0
    for game in input:
        ans += game.points()
    return ans

def solve_day04_part2(input: List[CardGame04]) -> Any:
    # card(inality) map
    card_map = {}
    # initialize all cards
    for i in range(len(input)):
        card_map[i + 1] = 1
    for game in input:
        id = game.id
        num_cards = card_map[id]
        num_matches = game.matches()
        for i in range(num_matches):
            new_card_id = id + i + 1
            if new_card_id in card_map:
                card_map[new_card_id] += num_cards
    return sum([card_map[id] for id in card_map])

def solve_day04(file_path: str, check_out: bool):
    input = parse_file_day04(file_path)
    out_part1 = solve_day04_part1(input)

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

    out_part2 = solve_day04_part2(input)
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

def main_04(run_all: bool = False):
    print("Running script for day 04")
    print("Sample input")
    solve_day04(sample_file_path, check_out=True)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day04(input_file_path, check_out=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_04(run_all=args.actual)
