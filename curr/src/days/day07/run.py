from typing import Tuple, List, Union

InputType = List[Tuple[int, List[int]]]
parent_path = "src/days/day07/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    _input = []
    with open(file_name, "r") as f:
        for line in f:
            target, rest = line.strip().split(": ")
            # Note that the target may show up multiple times :facepalm:
            _input.append((int(target), [int(v) for v in rest.split()]))
    return _input


def _debug(path, operands):
    p: List[Union[int, str]] = [operands[0]]
    for i in range(1, len(operands)):
        p = ["("] + p
        p.append(path[i - 1])
        p.append(operands[i])
        p = p + [")"]
    eq = "".join(str(v) for v in p)
    print(eq)


def _try_eq(target: int, operands: List[int]):
    def _walk(ind: int, curr: int, path: List[str]):
        if ind == len(operands):
            if target == curr:
                return True
            else:
                return False

        # try all operands
        return _walk(
            ind + 1,
            curr * operands[ind],
            path + ["*"],
        ) or _walk(
            ind + 1,
            curr + operands[ind],
            path + ["+"],
        )

    return _walk(1, operands[0], [])


def part1(_input: InputType) -> int:
    total = 0
    print(len(_input))
    instances = 0
    for target, operands in _input:
        if _try_eq(target, operands):
            total += target
            instances += 1
    print(instances)
    return total


def _try_eq_pt2(target: int, operands: List[int]):
    def _walk(ind: int, curr: int, path: List[str]):
        if ind == len(operands):
            if target == curr:
                return True
            else:
                return False

        # try all operands
        return (
            _walk(
                ind + 1,
                curr * operands[ind],
                path + ["*"],
            )
            or _walk(
                ind + 1,
                curr + operands[ind],
                path + ["+"],
            )
            or _walk(
                ind + 1,
                int(str(curr) + str(operands[ind])),
                path + ["||"],
            )
        )

    return _walk(1, operands[0], [])


def part2(_input: InputType) -> int:
    total = 0
    print(len(_input))
    instances = 0
    for target, operands in _input:
        if _try_eq_pt2(target, operands):
            total += target
            instances += 1
    print(instances)
    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
