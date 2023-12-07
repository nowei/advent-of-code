from typing import Any, Tuple, List
from collections import defaultdict
import argparse

sample_file_path = "test/07.sample"
input_file_path = "test/07.input"
expected_out_part1 = 6440
expected_out_part2 = 5905

class Hand07():
    bid: int
    hand: str
    rank: Tuple[int, int, int, int, int, int]

    # Note that we call the replacement of the Jack with the Joker `busted`,
    # not to be confused with running out of chips
    def hand_rank(hand: str, busted: bool = False) -> Tuple[int, int, int, int, int, int]:
        bucket = defaultdict(lambda: 0)
        card_rankings = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "T": 10,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        if busted:
            card_rankings["J"] = 1
        else:
            card_rankings["J"] = 11

        card_ranking = []
        for c in hand:
            bucket[c] += 1
            card_ranking.append(card_rankings[c])
        
        fives = False
        fours = False
        threes = False
        pairs = 0

        for c in bucket:
            if busted and c == "J":
                continue
            if bucket[c] == 5:
                fives = True
            elif bucket[c] == 4:
                fours = True
            elif bucket[c] == 3:
                threes += True
            elif bucket[c] == 2:
                pairs += 1

        rank = []
        if busted:
        # For busted computations, handle Joker cards separately
            jokers = bucket["J"]
            # 5s of the same, or 5 jokers, or 4 jokers + highcard or 3 jokers and a pair, or 2 jokers and a triple, or 1 joker and a fours
            # fours if of the same, 3 and a joker, a pair and two jokers, 1 and 3 jokers
            # full house if threes and pair, or 2 pairs and a joker
            # two pair if 2 pairs
            if jokers == 5: # always five of a kind
                rank.append(6)
            elif jokers == 4: # always 5 of a kind
                rank.append(6)
            elif jokers == 3: # two cards left
                if pairs == 1: # 5 of a kind
                    rank.append(6)
                else: # 2 cards different -> 4 of a kind
                    rank.append(5)
            elif jokers == 2:
                if threes: # five of a kind
                    rank.append(6)
                elif pairs == 1: # four of a kind
                    rank.append(5)
                else: # 3 cards different -> three of a kind
                    rank.append(3)
            elif jokers == 1:
                if fours: # five of a kind
                    rank.append(6)
                elif threes: # four of a kind
                    rank.append(5)
                elif pairs == 2: # full house
                    rank.append(4)
                elif pairs == 1: # three of a kind
                    rank.append(3)
                else: # one pair
                    rank.append(1)
            else: # jokers == 0
                if fives:
                    rank.append(6)
                elif fours:
                    rank.append(5)
                elif threes == 1 and pairs == 1:
                    # full house
                    rank.append(4)
                elif threes == 1:
                    rank.append(3)
                elif pairs == 2:
                    rank.append(2)
                elif pairs == 1:
                    rank.append(1)
                else:
                    # high card
                    rank.append(0)
        else:
            if fives:
                rank.append(6)
            elif fours:
                rank.append(5)
            elif threes and pairs == 1:
                # full house
                rank.append(4)
            elif threes:
                rank.append(3)
            elif pairs == 2:
                rank.append(2)
            elif pairs == 1:
                rank.append(1)
            else:
                # high card
                rank.append(0)
        rank.extend(card_ranking)
        return tuple(rank)
    
    def __init__(self, bid: int, hand: str):
        self.bid = bid
        self.hand = hand
        self.rank = Hand07.hand_rank(hand)
        self.busted_rank = Hand07.hand_rank(hand, busted=True)


def parse_file_day07(file_path) -> List[Hand07]:
    hands = []
    with open(file_path, "r") as f:
        for line in f:
            hand, bid_str = line.split()
            bid = int(bid_str)
            hands.append(Hand07(bid, hand))
    return hands

def solve_day07_part1(input: List[Hand07]) -> int:
    input.sort(key=lambda x: x.rank)
    ans = 0
    for i in range(len(input)):
        ans += (i+1)*input[i].bid
    return ans

def solve_day07_part2(input: List[Hand07]) -> int:
    input.sort(key=lambda x: x.busted_rank)
    ans = 0
    for i in range(len(input)):
        ans += (i+1)*input[i].bid
    return ans

def solve_day07(file_path: str, check_out: bool):
    input = parse_file_day07(file_path)
    out_part1 = solve_day07_part1(input)

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

    out_part2 = solve_day07_part2(input)
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

def main_07(run_all: bool = False):
    print("Running script for day 07")
    print("Sample input")
    solve_day07(sample_file_path, check_out=True)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day07(input_file_path, check_out=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_07(run_all=args.actual)
