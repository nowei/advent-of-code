from typing import List, Tuple, Dict, Any, Set
from heapq import heappop, heappush

InputType = Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]
parent_path = "src/days/day16/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        # file_name = parent_path + "sample.txt"
        file_name = parent_path + "sample2.txt"

    grid = []
    with open(file_name, "r") as f:
        for line in f:
            grid.append(list(line.strip()))
    start_pos = (0, 0)
    end_pos = (0, 0)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "S":
                start_pos = (row, col)
            elif grid[row][col] == "E":
                end_pos = (row, col)
    return grid, start_pos, end_pos


def dijkstras(grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]):
    heap = [(0, start, (0, 1))]
    visited = set()
    while heap:
        cost, curr, dir = heappop(heap)
        if curr == end:
            return cost
        if (
            curr in visited
        ):  # Already seen (possibly added multiple times due to evaluation being delayed to priority)
            continue
        visited.add(curr)
        row, col = curr
        # Check above, left, right, and below
        for n_dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            delta_row, delta_col = n_dir
            n_row, n_col = row + delta_row, col + delta_col
            if (n_row, n_col) in visited:
                continue
            if grid[n_row][n_col] == "#":
                continue
            n_cost = 1
            if dir != n_dir:
                n_cost += 1000
            heappush(heap, (n_cost + cost, (n_row, n_col), n_dir))
    return -1


def part1(_input: InputType) -> int:
    grid, start, end = _input
    best_path = dijkstras(grid, start, end)
    return best_path


def dijkstras_mutliple_paths(
    grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]
):
    heap = [(0, start, (0, 1), (start, (0, 1)))]
    visited = set()
    from_map: Dict[Tuple[Tuple[int, int], Tuple[int, int]], Any] = {}
    from_map[(start, (0, 1))] = {"cost": 0, "prevs": []}
    end_cost = 0
    while heap:
        cost, curr, dir, (prev, prev_dir) = heappop(heap)
        if curr == end:
            end_cost = cost
        if end_cost and cost > end_cost:
            break
        if (curr, dir) in from_map:
            if from_map[(curr, dir)]["cost"] == cost:
                from_map[(curr, dir)]["prevs"].append((prev, prev_dir))
        else:
            from_map[(curr, dir)] = {"cost": cost, "prevs": [(prev, prev_dir)]}

        if (
            (curr, dir) in visited
        ):  # Already seen (possibly added multiple times due to evaluation being delayed to priority)
            continue
        visited.add((curr, dir))
        row, col = curr
        # Check above, left, right, and below
        for n_dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            delta_row, delta_col = n_dir
            if dir == n_dir:
                n_cost = 1
                n_row, n_col = row + delta_row, col + delta_col
                if grid[n_row][n_col] == "#":
                    continue
                if (n_row, n_col) == prev:
                    continue
            else:
                n_cost = 1000
                n_row, n_col = row, col
            heappush(heap, (n_cost + cost, (n_row, n_col), n_dir, (curr, dir)))
    # Walk back
    visited_positions = set()
    curr_layer: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set(
        [(end, (0, 1)), (end, (-1, 0))]
    )
    while curr_layer:
        next_layer: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = set()
        for curr, dir in curr_layer:
            if (curr, dir) in visited_positions:
                continue
            visited_positions.add((curr, dir))
            print("visited", curr, dir, from_map.get((curr, dir)))
            for prev_step in from_map.get((curr, dir), {}).get("prevs", []):
                next_layer.add(prev_step)
        curr_layer = next_layer
    return set([p for p, d in visited_positions])


def visualize(grid: List[List[str]], visited: Set[Tuple[int, int]]):
    for row in range(len(grid)):
        line = ""
        for col in range(len(grid)):
            if (row, col) in visited:
                line += "O"
            else:
                line += grid[row][col]
        print(line)


def part2(_input: InputType) -> int:
    grid, start, end = _input
    best_seats = dijkstras_mutliple_paths(grid, start, end)
    visualize(grid, best_seats)
    return len(best_seats)


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
