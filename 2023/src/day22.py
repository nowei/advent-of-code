from typing import Any, Optional, Tuple, Dict, Set
from collections import defaultdict
import argparse

sample_file_path = "test/22.sample"
input_file_path = "test/22.input"


class Block22:
    block_id: int
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    def __init__(self, x1, y1, z1, x2, y2, z2, block_id):
        self.x1, self.y1, self.z1 = x1, y1, z1
        self.x2, self.y2, self.z2 = x2, y2, z2
        self.block_id = block_id

    def clone(self):
        return Block22(
            self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, self.block_id
        )


class Setting22:
    blocks: Dict[int, Block22]
    supported_blocks: Dict[int, Set[str]]
    filled_blocks: Dict[Tuple[int, int, int], int]

    def __init__(self, blocks):
        self.blocks = blocks

    # returns the number of moved blocks
    def resolve(self) -> int:
        # fall down
        # on each z layer, bring blocks down as much as possible
        # Keep track of each (x, y) for each letter.
        # if there is a letter under an space, the new height gets
        # shifted down as much as possible.
        # If there are no letters below (x, y), z = 1,
        # otherwise the bottom gets shifted to max(z(shape) for shape in below-set) + 1
        fallen_down = {}
        supported_blocks = {}
        self.filled_blocks = {}
        moved = 0
        # Sort blocks by order in which they should fall down according to the snapshot
        for b_id in sorted(self.blocks.keys(), key=lambda x: self.blocks[x].z1):
            # new_start, new_end
            level_set = set()
            supported_cand_set = set()
            b = self.blocks[b_id]
            for x in range(b.x1, b.x2 + 1):
                for y in range(b.y1, b.y2 + 1):
                    level_set.add((x, y))
                    if (x, y) in fallen_down:
                        supported_cand_set.add(fallen_down[(x, y)])
                    fallen_down[(x, y)] = b.block_id
            max_z = max([self.blocks[ob].z2 for ob in supported_cand_set] + [0])
            start_z = max_z + 1  # move block down from z1 to start_z
            if start_z != b.z1:
                moved += 1
            z_diff = b.z2 - b.z1
            b.z1 = start_z
            b.z2 = start_z + z_diff
            for z in range(b.z1, b.z2 + 1):
                for x, y in level_set:
                    assert (x, y, z) not in self.filled_blocks
                    self.filled_blocks[(x, y, z)] = b_id
            supported_set = set()
            # actually check below set to see what is supported
            for x, y in level_set:
                cand = (x, y, max_z)
                if cand in self.filled_blocks:
                    supported_set.add(self.filled_blocks[cand])
            supported_blocks[b_id] = supported_set
        self.supported_blocks = supported_blocks
        return moved

    def clone(self) -> "Setting22":
        new_blocks = {}
        for b in self.blocks:
            new_blocks[b] = self.blocks[b].clone()
        return Setting22(new_blocks)

    def get_disintegrated_cands(self):
        disintegrate_cands = set()
        supports = defaultdict(lambda: set())
        for b_id in self.blocks:
            for support in self.supported_blocks[b_id]:
                supports[support].add(b_id)

        for b_id in self.blocks:
            valid = True
            # if all things above were supported by at least one other block, then can still be disintegrated
            for ob_id in supports[b_id]:
                if len(self.supported_blocks[ob_id]) == 1:
                    valid = False
                    break
            # if it supports no blocks, can also be disintegrated
            if valid:
                disintegrate_cands.add(b_id)
        return disintegrate_cands


def parse_file_day22(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    blocks = {}
    b_id = 0
    for line in lines:
        curr = line.strip()
        coords = [[int(v) for v in l.split(",")] for l in curr.split("~")]
        x1, y1, z1 = coords[0]
        x2, y2, z2 = coords[1]
        b = Block22(x1, y1, z1, x2, y2, z2, b_id)
        b_id += 1
        blocks[b.block_id] = b
    return Setting22(blocks)


def solve_day22_part1(input: Setting22) -> int:
    input.resolve()
    return len(input.get_disintegrated_cands())


def solve_day22_part2(input: Setting22) -> int:
    input.resolve()
    disintegrated_cands = input.get_disintegrated_cands()
    total = 0
    for b in input.blocks:
        if b in disintegrated_cands:
            continue
        cand = input.clone()
        cand.blocks.pop(b)
        total += cand.resolve()
    return total


def solve_day22(
    input: Setting22,
    expected_pt1: Optional[int] = None,
    expected_pt2: Optional[int] = None,
):
    out_part1 = solve_day22_part1(input)

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

    out_part2 = solve_day22_part2(input)
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


def main_22(
    run_all: bool = False, example: Optional[str] = None, answer_only: bool = False
):
    if not answer_only:
        if example:
            print("Testing input from cmd line")
            input = parse_file_day22("", example=example)
            solve_day22(input)
            exit(0)

        print("Running script for day 22")
        print("Sample input")
        print("---------------------------------")
        expected_out_part1 = 5
        expected_out_part2 = 7
        print("Input file:", sample_file_path)
        input = parse_file_day22(sample_file_path)
        solve_day22(
            input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2
        )

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day22(input_file_path)
        # p1: 464 is too high
        solve_day22(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--actual", action="store_true")
    parser.add_argument("-e", "--example")
    parser.add_argument("-o", "--answer-only", action="store_true")
    args = parser.parse_args()
    main_22(run_all=args.actual, example=args.example, answer_only=args.answer_only)
