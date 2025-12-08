from typing import List, Tuple
import math
from collections import Counter

InputType = Tuple[List[List[int]], int]
parent_path = "src/days/day08/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    num_connections = 1000
    if sample:
        file_name = parent_path + "sample.txt"
        num_connections = 10
    coords = []
    with open(file_name, "r") as f:
        for line in f:
            coords.append([int(v) for v in line.strip().split(",")])
    return coords, num_connections


def part1(_input: InputType) -> int:
    coords, num_connections = _input
    # some sort of union find
    groupings = [i for i in range(len(coords))]
    pairwise_distances: List[List[float]] = []
    for i in range(len(coords)):
        pairwise_distances.append([])
        for j in range(len(coords)):
            if i == j:
                pairwise_distances[-1].append(0)
            else:
                xi, yi, zi = coords[i]
                xj, yj, zj = coords[j]
                pairwise_distances[-1].append(
                    math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2)
                )
    candidates = []
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            candidates.append((i, j))
    candidates.sort(key=lambda x: pairwise_distances[x[0]][x[1]])
    for con in range(num_connections):
        i, j = candidates[con]
        orig = max(groupings[i], groupings[j])
        new_val = min(groupings[i], groupings[j])
        groupings[j] = new_val
        groupings[i] = new_val
        for idx in range(len(groupings)):
            if groupings[idx] == orig:
                groupings[idx] = new_val
    counts = Counter(groupings)
    print(counts)
    result = 1
    for _group, count in counts.most_common(3):
        result *= count
    return result


def part2(_input: InputType) -> int:
    coords, num_connections = _input
    # some sort of union find
    groupings = [i for i in range(len(coords))]
    pairwise_distances: List[List[float]] = []
    for i in range(len(coords)):
        pairwise_distances.append([])
        for j in range(len(coords)):
            if i == j:
                pairwise_distances[-1].append(0)
            else:
                xi, yi, zi = coords[i]
                xj, yj, zj = coords[j]
                pairwise_distances[-1].append(
                    math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2)
                )
    candidates = []
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            candidates.append((i, j))
    curr_counter = Counter(groupings)
    candidates.sort(key=lambda x: pairwise_distances[x[0]][x[1]])
    con = 0
    while True:
        i, j = candidates[con]
        orig = max(groupings[i], groupings[j])
        new_val = min(groupings[i], groupings[j])
        groupings[j] = new_val
        groupings[i] = new_val
        for idx in range(len(groupings)):
            if groupings[idx] == orig:
                groupings[idx] = new_val
        con += 1
        new_counter = Counter(groupings)
        if len(curr_counter) == 2 and len(new_counter) == 1:
            break
        curr_counter = new_counter
    xi, _, _ = coords[i]
    xj, _, _ = coords[j]
    return xi * xj


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
