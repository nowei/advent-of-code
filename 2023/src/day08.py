from typing import Any, Dict
import argparse
import numpy as np

sample_file_path = "test/08.sample"
sample_part2_file_path = "test/08.sample2"
input_file_path = "test/08.input"
expected_out_part1 = 2
expected_out_part2 = 6


class Node08:
    value: str
    left: str
    right: str

    def __init__(self, value: str, left: str, right: str):
        self.value = value
        self.left = left
        self.right = right


class Map08:
    instructions: str
    nodes: Dict[str, Node08]

    def __init__(self, instructions: str, nodes: Dict[str, Node08]):
        self.instructions = instructions
        self.nodes = nodes


def parse_file_day08(file_path) -> Any:
    nodes = {}
    with open(file_path, "r") as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f:
            value, left_right = line.strip().split(" = ")
            left, right = left_right.strip("()").split(", ")
            node = Node08(value, left, right)
            nodes[value] = node
    return Map08(instructions, nodes)


def solve_day08_part1(input: Map08) -> int:
    steps = 0
    value = "AAA"
    while value != "ZZZ":
        inst = input.instructions[steps % len(input.instructions)]
        if inst == "R":
            value = input.nodes[value].right
        else:
            value = input.nodes[value].left
        steps += 1
    return steps


def solve_day08_part2(input: Map08) -> int:
    steps = 0
    values = set()
    # get all values ending in 0
    # An observation is that we only care about sets, so if they eventually cycle, we can track less values
    # Another observation is that if they don't cycle, we only need to follow the paths until they cycle or track when they reach a Z.
    for k in input.nodes:
        if k.endswith("A"):
            values.add(k)

    cycles = {}
    lcm_input = []
    for k in values:
        curr = k
        cycles[k] = []
        seen = set()
        path = []
        steps = 0
        while True:
            step_index = steps % len(input.instructions)
            inst = input.instructions[step_index]
            if (step_index, curr) in seen:
                break
            path.append((step_index, curr))
            seen.add((step_index, curr))
            if inst == "R":
                curr = input.nodes[curr].right
            else:
                curr = input.nodes[curr].left
            steps += 1
            # Second condition is to not include repeated cycles
            if curr.endswith("Z") and (step_index, curr) not in seen:
                cycles[k].append((steps, curr))
                lcm_input.append(steps)
        # cycling starts with curr
        path_cycle_start = curr
        print(
            path_cycle_start,
            path.index((step_index, curr)),
            len(path),
            len(seen),
            cycles[k],
        )
        # print(path)

    return np.lcm.reduce(lcm_input)


def solve_day08(file_path: str, check_out: bool):
    input = parse_file_day08(file_path)
    out_part1 = solve_day08_part1(input)

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

    if "sample" in file_path:
        input = parse_file_day08(sample_part2_file_path)
    out_part2 = solve_day08_part2(input)
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


def main_08(run_all: bool = False):
    print("Running script for day 08")
    print("Sample input")
    solve_day08(sample_file_path, check_out=True)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        solve_day08(input_file_path, check_out=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--actual", action="store_true")
    args = parser.parse_args()
    main_08(run_all=args.actual)
