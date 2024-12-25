from typing import List, Tuple

InputType = Tuple[List[List[int]], List[List[int]]]
parent_path = "src/days/day25/"


def _parse_input(sample: bool) -> Tuple[List[List[int]], List[List[int]]]:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    keys = []
    locks = []
    with open(file_name, "r") as f:
        key_locks: List[List[str]] = [[]]
        for line in f:
            if line.strip() == "":
                key_locks.append([])
                continue
            key_locks[-1].append(line.strip())
        for key_lock in key_locks:
            curr = []
            if key_lock[0][0] == "#":
                for col in range(len(key_lock[0])):
                    for row in range(len(key_lock)):
                        if key_lock[row][col] == ".":
                            break
                    curr.append(row)
                locks.append(curr)
            else:
                for col in range(len(key_lock[0])):
                    for row in range(len(key_lock) - 1, -1, -1):
                        if key_lock[row][col] == ".":
                            break
                    curr.append(len(key_lock) - 1 - row)
                keys.append(curr)
    print(locks)
    print(keys)
    print(len(key_locks))
    return keys, locks


def part1(_input: InputType) -> int:
    keys, locks = _input
    total = 0
    for key in keys:
        for lock in locks:
            curr = []
            for i in range(len(key)):
                curr.append(key[i] + lock[i])
            print(curr)
            if all(c <= 7 for c in curr):
                total += 1
    return total


def part2(_input: InputType) -> int:
    return 0


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
