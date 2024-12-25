from typing import List, Tuple, Set, Union

InputType = Tuple[Tuple[int, int], List[Tuple[int, int]], int]
parent_path = "src/days/day18/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    size = (71, 71)
    falling = 1024
    if sample:
        file_name = parent_path + "sample.txt"
        size = (7, 7)
        falling = 12

    coords = []
    with open(file_name, "r") as f:
        for line in f:
            a, b = line.strip().split(",")
            coords.append((int(a), int(b)))
    return size, coords, falling


def visualize(
    size: Tuple[int, int], corrupted: Set[Tuple[int, int]], path: Set[Tuple[int, int]]
):
    for y in range(size[1]):
        line = ""
        for x in range(size[0]):
            if (x, y) in corrupted:
                line += "#"
            elif (x, y) in path:
                line += "O"
            else:
                line += "."
        print(line)


def find_path(
    size: Tuple[int, int], falling_bytes: List[Tuple[int, int]], falling: int
) -> Set[Tuple[int, int]]:
    start = (0, 0)
    end = (size[0] - 1, size[1] - 1)
    seen = set()
    path_map = {}
    layer: Set[Tuple[int, int]] = set([start])
    fallen_bytes = set(falling_bytes[:falling])
    while layer:
        new_layer = set()
        for x, y in layer:
            seen.add((x, y))
            for x_d, y_d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                c_x = x + x_d
                c_y = y + y_d
                if c_x < 0 or c_x >= size[0]:
                    continue
                if c_y < 0 or c_y >= size[1]:
                    continue
                if (c_x, c_y) in fallen_bytes:
                    continue
                if (c_x, c_y) in seen:
                    continue
                path_map[(c_x, c_y)] = x, y
                new_layer.add((c_x, c_y))
        layer = new_layer
    path = []
    curr = end
    while curr in path_map:
        path.append(curr)
        curr = path_map[curr]
    path.append(curr)
    return set(path)


def part1(_input: InputType) -> int:
    size, falling_bytes, falling = _input
    path = find_path(size, falling_bytes, falling)
    visualize(size, set(falling_bytes[:falling]), path)
    return len(path) - 1


def find_breaking(
    size: Tuple[int, int], falling_bytes: List[Tuple[int, int]], falling_idx: int
) -> Tuple[int, int]:
    start = (0, 0)
    end = (size[0] - 1, size[1] - 1)
    fallen_bytes = set(falling_bytes[:falling_idx])
    last_added_byte = falling_bytes[falling_idx - 1]
    while True:
        seen = set()
        path_map = {}
        layer: Set[Tuple[int, int]] = set([start])
        while layer:
            new_layer = set()
            for x, y in layer:
                seen.add((x, y))
                for x_d, y_d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    c_x = x + x_d
                    c_y = y + y_d
                    if c_x < 0 or c_x >= size[0]:
                        continue
                    if c_y < 0 or c_y >= size[1]:
                        continue
                    if (c_x, c_y) in fallen_bytes:
                        continue
                    if (c_x, c_y) in seen:
                        continue
                    path_map[(c_x, c_y)] = x, y
                    new_layer.add((c_x, c_y))
            layer = new_layer
        path = []
        curr = end
        if end not in path_map:
            break
        while curr in path_map:
            path.append(curr)
            curr = path_map[curr]
        path.append(curr)
        path_set = set(path)
        while last_added_byte not in path_set and falling_idx < len(falling_bytes):
            falling_idx += 1
            last_added_byte = falling_bytes[falling_idx]
            fallen_bytes.add(last_added_byte)

    return last_added_byte


def part2(_input: InputType) -> str:
    size, falling_bytes, falling = _input
    breaking = find_breaking(size, falling_bytes, falling)
    return f"{breaking[0]},{breaking[1]}"


def exec(part: int, execute: bool) -> Union[int, str]:
    _input = _parse_input(not execute)
    result: Union[int, str] = 0
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
