
from typing import Any, Dict, List
import argparse

sample_file_path = "test/02.sample"
input_file_path = "test/02.input"
expected_out_part1 = 8
expected_out_part2 = 2286

class Game02Instance:
    blue: int
    red: int
    green: int

    def __init__(self, red=0, blue=0, green=0):
        self.red = red
        self.blue = blue
        self.green = green
    
    def check_exceeds(self, game_rule: "Game02Instance") -> bool:
        if self.red > game_rule.red:
            return True
        if self.blue > game_rule.blue:
            return True
        if self.green > game_rule.green:
            return True
        return False
    
class Game02:
    id: int
    game_instances: List[Game02Instance]

    def __init__(self, id: int, game_instances: List[Game02Instance]):
        self.id = id
        self.game_instances = game_instances
    
    def check_exceeds(self, game_rule: Game02Instance) -> bool:
        for game in self.game_instances:
            if game.check_exceeds(game_rule):
                return True
        return False

    def power(self) -> int:
        max_dict = {"red": 0, "green": 0, "blue": 0}
        for game in self.game_instances:
            max_dict["red"] = max(max_dict["red"], game.red)
            max_dict["blue"] = max(max_dict["blue"], game.blue)
            max_dict["green"] = max(max_dict["green"], game.green)
        
        return max_dict["red"] * max_dict["blue"] * max_dict["green"]


def parse_file_day02(file_path) -> Dict[int, Game02]:
    games_dict = {}
    with open(file_path, "r") as f:
        for line in f:
            game_id_str, games_str = line.split(":")
            game_id = int(game_id_str.split()[1])
            # This can be a better regex
            games = []
            for game_str in games_str.split(";"):
                game_instance_dict = {}
                for pair in game_str.split(","):
                    num_str, color = pair.strip().split()
                    game_instance_dict[color] = int(num_str)
                games.append(Game02Instance(**game_instance_dict))
            games_dict[game_id] = Game02(game_id, games)
    return games_dict

def solve_day02_part1(input: Dict[int, Game02]) -> int:
    ans = 0
    game_rule = Game02Instance(red=12, green=13, blue=14)
    for id in input:
        if not input[id].check_exceeds(game_rule):
            ans += id
    return ans

def solve_day02_part2(input: Dict[int, Game02]) -> int:
    ans = 0
    for id in input:
        ans += input[id].power()
    return ans

def solve_day02(file_path: str, check_out: bool):
    input = parse_file_day02(file_path)
    out_part1 = solve_day02_part1(input)

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

    out_part2 = solve_day02_part2(input)
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

def main_02(run_all: bool = False):
    print("Running script for day 02")
    print("Sample input")
    solve_day02(sample_file_path, check_out=True)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day02(input_file_path, check_out=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_02(run_all=args.actual)
