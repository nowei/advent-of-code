from typing import List, Tuple

InputType = List[List[str]]
parent_path = "src/days/day04/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    inp = []
    with open(file_name, "r") as f:
        for line in f:
            inp.append(list(line.strip()))
    return inp


def _search_part1(_input: InputType, word: str):
    # If it starts with the first letter, run search in all the directions

    def _search(
        init_pos: Tuple[int, int], direction: Tuple[int, int], word: str, ind: int
    ):
        row, col = init_pos
        dir_row, dir_col = direction
        cand_row, cand_col = row + dir_row * ind, col + dir_col * ind
        if cand_row < 0 or cand_row >= len(_input):
            return 0
        if cand_col < 0 or cand_col >= len(_input[0]):
            return 0
        if word[ind] == _input[cand_row][cand_col]:
            if ind == len(word) - 1:
                return 1
            else:
                return _search(init_pos, direction, word, ind + 1)
        return 0

    def _kick_off_search(init_pos: Tuple[int, int], word: str):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                count += _search(init_pos, (i, j), word, 1)
        return count

    total = 0
    for row in range(len(_input)):
        for col in range(len(_input[0])):
            if _input[row][col] == word[0]:
                total += _kick_off_search((row, col), word)
    return total


def part1(_input: InputType) -> int:
    # Look for XMAS in directions
    result = _search_part1(_input, "XMAS")
    return result


def _search_part2(_input: InputType, three_letter_word: str):
    def _search(init_pos: Tuple[int, int], word: str):
        # Check diagonals
        valid = 0
        row, col = init_pos
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                if row + i < 0 or row + i >= len(_input):
                    continue
                if row - i < 0 or row - i >= len(_input):
                    continue
                if col + j < 0 or col + j >= len(_input[0]):
                    continue
                if col - j < 0 or col - j >= len(_input[0]):
                    continue

                if _input[row + i][col + j] == "M" and _input[row - i][col - j] == "S":
                    valid += 1
        return valid == 2

    center = three_letter_word[1]
    total = 0
    for row in range(len(_input)):
        for col in range(len(_input[0])):
            if _input[row][col] == center:
                total += _search((row, col), three_letter_word)
    return total


def part2(_input: InputType) -> int:
    # Look for center "A"s and look for an M and an S
    result = _search_part2(_input, "MAS")
    return result


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
