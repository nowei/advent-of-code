from functools import cache
from typing import List, Dict, Tuple
from collections import OrderedDict, Counter

InputType = List[str]
parent_path = "src/days/day21/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
        # file_name = parent_path + "sample2.txt"
    codes = []
    with open(file_name, "r") as f:
        for line in f:
            codes.append(line.strip())
    return codes


def precompute_paths() -> Dict[str, Dict[str, List[str]]]:
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    keypad = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        ["#", "0", "A"],
    ]
    directional = [
        ["#", "^", "A"],
        ["<", "v", ">"],
    ]

    def bfs(grid: List[List[str]], row: int, col: int) -> Dict[str, List[str]]:
        _c = grid[row][col]
        curr_layer = [(row, col, "")]
        path: Dict[str, List[str]] = {}
        while curr_layer:
            new_layer = []
            for row, col, p in curr_layer:
                new_c = grid[row][col]
                if new_c == "#":
                    continue
                if new_c in path:
                    if len(p) == len(path[new_c][0]):
                        path[new_c].append(p)
                    else:
                        continue
                else:
                    path[new_c] = [p]
                for d_row, d_col, np in sorted(
                    [
                        (0, 1, ">"),
                        (0, -1, "<"),
                        (1, 0, "v"),
                        (-1, 0, "^"),
                    ],
                    key=lambda x: not (p and x[2][-1] == p),
                ):
                    n_row, n_col = d_row + row, d_col + col
                    if n_row < 0 or n_row >= len(grid):
                        continue
                    if n_col < 0 or n_col >= len(grid[0]):
                        continue
                    new_layer.append((n_row, n_col, p + np))
            curr_layer = new_layer

        return path

    paths: Dict[str, Dict[str, List[str]]] = {}
    for row in range(len(keypad)):
        for col in range(len(keypad[1])):
            c = keypad[row][col]
            path = bfs(keypad, row, col)
            paths[c] = path
    # Eliminate bad possibilities
    for p in paths:
        for target in paths[p]:
            current_paths = paths[p][target]
            if not current_paths[0]:
                continue
            new_candidate_paths = []
            for candidate_path in current_paths:
                c = candidate_path[0]
                changes = 0
                for val in candidate_path[1:]:
                    if val != c:
                        changes += 1
                    c = val
                if changes <= 1:
                    new_candidate_paths.append(candidate_path)
            paths[p][target] = new_candidate_paths

    # paths["0"]["7"] = "^^^<"
    # paths["A"]["1"] = "^<<"
    # paths["A"]["4"] = "^^<<"
    # paths["A"]["7"] = "^^^<<"
    # print(paths)
    directional_paths = {}
    for row in range(len(directional)):
        for col in range(len(directional[1])):
            c = directional[row][col]
            path = bfs(directional, row, col)
            directional_paths[c] = path
    # Eliminate bad possibilities
    for p in directional_paths:
        for target in directional_paths[p]:
            current_paths = directional_paths[p][target]
            if not current_paths[0]:
                continue
            new_candidate_paths = []
            for candidate_path in current_paths:
                c = candidate_path[0]
                changes = 0
                for val in candidate_path[1:]:
                    if val != c:
                        changes += 1
                    c = val
                if changes <= 1:
                    new_candidate_paths.append(candidate_path)
            directional_paths[p][target] = new_candidate_paths
    # print(directional_paths)
    for p in directional_paths:
        if p in paths:
            paths[p] |= directional_paths[p]
        else:
            paths[p] = directional_paths[p]

    return paths


def process_code(code, paths):
    # keypad robot <- directional robot
    prev = "A"
    starting = code
    cand = []
    transitions = []
    for c in starting:
        cand.append(paths[prev][c])
        transitions.append((prev, c))
        prev = c
    od: Dict[Tuple[str, str], int] = OrderedDict()
    for t in transitions:
        od[t] = od.get(t, 0) + 1
    print(od)
    starting = "".join(cand)
    print(starting)
    cand = []
    prev = "A"
    transitions = []
    # directional robot <- directional robot
    for c in starting:
        cand.append(paths[prev][c])
        transitions.append((prev, c))
        prev = c
    od = OrderedDict()
    for t in transitions:
        od[t] = od.get(t, 0) + 1
    print(od)

    starting = "".join(cand)
    print(starting)
    cand = []
    prev = "A"
    transitions = []
    # directional robot <- you
    for c in starting:
        cand.append(paths[prev][c])
        transitions.append((prev, c))
        # cand_str += paths[c]["A"]
        prev = c
    od = OrderedDict()
    for t in transitions:
        od[t] = od.get(t, 0) + 1
    print(od)
    # print(p1)
    # print(p2)
    # print(p3)
    return "".join(cand)


# Ayo this works!!!
# For each potential path from a -> b,
# optimize for ending distance closest to the enter (A) key.
def optimize(paths: Dict[str, Dict[str, List[str]]]) -> Dict[str, Dict[str, str]]:
    optimized_paths: Dict[str, Dict[str, str]] = {}
    distance_from_a = {"<": 3, "^": 1, "v": 2, ">": 1}
    for p in ["<", ">", "^", "v", "A"]:
        optimized_paths[p] = {}
        current_start = paths[p]
        for t in ["<", ">", "^", "v", "A"]:
            current_end = current_start[t]
            best = current_end[0]
            for candidate in current_end[1:]:
                # Play every movement
                if distance_from_a[candidate[-1]] < distance_from_a[best[-1]]:
                    best = candidate
            optimized_paths[p][t] = best + "A"
    for p in [str(i) for i in range(10)] + ["A"]:
        if p not in optimized_paths:
            optimized_paths[p] = {}
        current_start = paths[p]
        for t in [str(i) for i in range(10)] + ["A"]:
            current_end = current_start[t]
            best = current_end[0]
            for candidate in current_end[1:]:
                # Play every movement
                if distance_from_a[candidate[-1]] < distance_from_a[best[-1]]:
                    best = candidate
            optimized_paths[p][t] = best + "A"
    # print(optimized_paths)
    return optimized_paths


# 223838 -- too high
# 212678 -- too low
def part1(_input: InputType) -> int:
    codes = _input
    paths = precompute_paths()
    optimized_paths = optimize(paths)
    total = 0
    for code in codes:
        print(code)
        candidate = process_code(code, optimized_paths)
        print(candidate, len(candidate), "\n")
        total += len(candidate) * int(code.strip("A"))
    return total


level_set: Dict[int, Dict[Tuple[str, str], int]] = {}


def process_code_count_transitions(code, paths, translations: int):
    # keypad robot <- 1st directional robot
    starting = "A" + code
    transitions = []
    for i in range(1, len(starting)):
        # Translated move for first directional robot
        prev, curr = starting[i - 1], starting[i]
        # Where the keypad robot stops
        transitions.append((prev, curr))
    prev_transitions: Dict[Tuple[str, str], int] = OrderedDict()
    for t in transitions:
        prev_transitions[t] = prev_transitions.get(t, 0) + 1
    for _i in range(translations):
        transitioned: Dict[Tuple[str, str], int] = OrderedDict()
        path_counter: Dict[str, int] = Counter()
        for (start, end), count in prev_transitions.items():
            next_path = paths[start][end]
            path_counter[next_path] += count
        for path, count in path_counter.items():
            n_path = "A" + path
            for i in range(1, len(n_path)):
                prev, curr = n_path[i - 1], n_path[i]
                transitioned[(prev, curr)] = transitioned.get((prev, curr), 0) + count
        prev_transitions = transitioned
    ops = sum(v for v in transitioned.values())

    return ops


def walk(path: str, paths: Dict[str, Dict[str, List[str]]], levels: int) -> int:
    @cache
    def walk_path(level: int, path: str) -> int:
        if level == 0:
            return len(path)
        current_total = 0
        n_path = "A" + path
        for i in range(1, len(n_path)):
            prev, curr = n_path[i - 1], n_path[i]
            current_best = float("inf")
            for cand in paths[prev][curr]:
                val = walk_path(level - 1, cand + "A")
                if val < current_best:
                    current_best = val
            current_total += int(current_best)
            if level in level_set:
                level_set[level][(prev, curr)] = int(current_best)
            else:
                level_set[level] = {(prev, curr): int(current_best)}
        return current_total

    return walk_path(levels, path)


# 219254 is the right one for indirections=3
# 301594324799984 -- too high
# 264518225304496 is the right answer
# 120483996171680 -- too low
def part2(_input: InputType) -> int:
    codes = _input
    paths = precompute_paths()
    optimized_paths = optimize(paths)
    print(optimized_paths)
    total = 0
    total2 = 0
    steps = 26
    for code in codes:
        print(code)
        candy = walk(code, paths, steps)
        total2 += candy * int(code.strip("A"))
        candidate = process_code_count_transitions(
            code, optimized_paths, translations=steps
        )
        total += candidate * int(code.strip("A"))
        print(candy, candidate)
    print(total2, total)
    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
