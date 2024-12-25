from typing import List, Dict, Tuple, Set
from collections import defaultdict

InputType = List[List[str]]
parent_path = "src/days/day08/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    _map = []
    with open(file_name, "r") as f:
        for line in f:
            _map.append(list(line.strip()))
    return _map


def _derive_antenna_groups(_input: InputType) -> Dict[str, List[Tuple[int, int]]]:
    mapping = defaultdict(list)
    for row in range(len(_input)):
        for col in range(len(_input[0])):
            frequency = _input[row][col]
            if frequency != ".":
                mapping[frequency].append((row, col))
    return mapping


def _derive_antinode_groups(
    antenna_groups: Dict[str, List[Tuple[int, int]]], max_row: int, max_col: int
) -> Dict[str, List[Tuple[int, int]]]:
    result = {}
    for key, group in antenna_groups.items():
        cand_list = []
        for a in range(len(group) - 1):
            for b in range(a + 1, len(group)):
                a_row, a_col = group[a]
                b_row, b_col = group[b]
                # a -> b
                diff_row = b_row - a_row
                diff_col = b_col - a_col
                cand_list.append((b_row + diff_row, b_col + diff_col))
                cand_list.append((a_row - diff_row, a_col - diff_col))
        result[key] = [
            (row, col)
            for row, col in cand_list
            if ((row >= 0 and row < max_row) and (col >= 0 and col < max_col))
        ]
    return result


def part1(_input: InputType) -> int:
    antenna_groups = _derive_antenna_groups(_input)
    max_row, max_col = len(_input), len(_input[0])
    antinode_groups = _derive_antinode_groups(antenna_groups, max_row, max_col)
    antinode_locations: Set[Tuple[int, int]] = set()
    for group in antinode_groups.values():
        antinode_locations |= set(group)
    return len(antinode_locations)


def _derive_antinode_groups_pt2(
    antenna_groups: Dict[str, List[Tuple[int, int]]], max_row: int, max_col: int
) -> Dict[str, List[Tuple[int, int]]]:
    result = {}
    for key, group in antenna_groups.items():
        cand_list = []
        for a in range(len(group) - 1):
            for b in range(a + 1, len(group)):
                a_row, a_col = group[a]
                b_row, b_col = group[b]
                # a -> b
                diff_row = b_row - a_row
                diff_col = b_col - a_col
                while b_row >= 0 and b_col >= 0 and b_row < max_row and b_col < max_col:
                    b_row += diff_row
                    b_col += diff_col
                    cand_list.append((b_row, b_col))
                while a_row >= 0 and a_col >= 0 and a_row < max_row and a_col < max_col:
                    a_row -= diff_row
                    a_col -= diff_col
                    cand_list.append((a_row, a_col))
        result[key] = [
            (row, col)
            for row, col in cand_list
            if ((row >= 0 and row < max_row) and (col >= 0 and col < max_col))
        ]
    return result


def _print_map(_input: InputType, antinode_locations: Set[Tuple[int, int]]):
    for row in range(len(_input)):
        c_row = []
        for col in range(len(_input[0])):
            if _input[row][col] == "." and (row, col) in antinode_locations:
                c_row.append("#")
            else:
                c_row.append(_input[row][col])
        print("".join(c_row))


def part2(_input: InputType) -> int:
    antenna_groups = _derive_antenna_groups(_input)
    max_row, max_col = len(_input), len(_input[0])
    antinode_groups = _derive_antinode_groups_pt2(antenna_groups, max_row, max_col)
    antinode_locations: Set[Tuple[int, int]] = set()
    for key, group in antinode_groups.items():
        antinode_locations |= set(group) | set(antenna_groups[key])
    _print_map(_input, antinode_locations)
    return len(antinode_locations)


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
