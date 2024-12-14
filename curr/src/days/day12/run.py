from typing import List, Dict, Tuple
from collections import Counter, defaultdict

InputType = List[List[str]]
parent_path = "src/days/day12/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    result = []
    with open(file_name, "r") as f:
        for line in f:
            result.append(list(line.strip()))
    return result


def _walk(
    grid: InputType,
    row: int,
    col: int,
    plot: str,
    plot_assignment: str,
    attribution: Dict[Tuple[int, int, str], str],
):
    def walk(row, col):
        curr_plot = grid[row][col]
        if curr_plot != plot:  # Adjacent plot not the current plot
            return 1, 0
        if (row, col, curr_plot) in attribution:  # Already seen
            return 0, 0
        # Check cardinals
        attribution[row, col, curr_plot] = plot_assignment
        perimeter = 0
        area = 1
        if row - 1 < 0:
            perimeter += 1
        else:
            north_perim, north_area = walk(row - 1, col)
            perimeter += north_perim
            area += north_area
        if col - 1 < 0:
            perimeter += 1
        else:
            west_perim, west_area = walk(row, col - 1)
            perimeter += west_perim
            area += west_area
        if row + 1 >= len(grid):
            perimeter += 1
        else:
            south_perim, south_area = walk(row + 1, col)
            perimeter += south_perim
            area += south_area
        if col + 1 >= len(grid):
            perimeter += 1
        else:
            east_perim, east_area = walk(row, col + 1)
            perimeter += east_perim
            area += east_area

        return perimeter, area

    return walk(row, col)


def count_grid_area_perim(grid: InputType):
    area: Dict[str, int] = Counter()
    perimeter: Dict[str, int] = Counter()
    attribution: Dict[Tuple[int, int, str], str] = {}
    seen_groups: Dict[str, int] = {}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            plot = grid[row][col]
            if (row, col, plot) in attribution:
                continue
            if plot in seen_groups:
                plot_assignment = f"{plot}{seen_groups[plot]}"
                seen_groups[plot] += 1
            else:
                plot_assignment = f"{plot}0"
                seen_groups[plot] = 1
            plot_perimeter, plot_area = _walk(
                grid,
                row,
                col,
                plot,
                plot_assignment,
                attribution,
            )
            area[plot_assignment] = plot_area
            perimeter[plot_assignment] = plot_perimeter
    print(area)
    print(perimeter)
    return area, perimeter, attribution


def part1(_input: InputType) -> int:
    area, perimeter, _attribution = count_grid_area_perim(_input)
    total = 0
    for key in area:
        total += area[key] * perimeter[key]
    return total


def process_group(group: List[Tuple[int, int]]) -> int:
    contiguous_rows: List[List[Tuple[int, int]]] = [[]]
    contiguous_columns: List[List[Tuple[int, int]]] = [[]]
    group_set = set(group)
    sorted_rows = sorted(group, key=lambda x: (x[0], x[1]))
    sorted_cols = sorted(group, key=lambda x: (x[1], x[0]))
    prev_pos = sorted_rows[0]
    contiguous_rows[-1].append(prev_pos)
    for curr_pos in sorted_rows[1:]:
        if prev_pos[0] == curr_pos[0] and prev_pos[1] == curr_pos[1] - 1:
            contiguous_rows[-1].append(curr_pos)
        else:  # there is a gap or there is a new row
            contiguous_rows.append([curr_pos])
        prev_pos = curr_pos
    prev_pos = sorted_cols[0]
    contiguous_columns[-1].append(prev_pos)
    for curr_pos in sorted_cols[1:]:
        if prev_pos[1] == curr_pos[1] and prev_pos[0] == curr_pos[0] - 1:
            contiguous_columns[-1].append(curr_pos)
        else:  # there is a gap or there is a new row
            contiguous_columns.append([curr_pos])
        prev_pos = curr_pos
    sides = 0
    print("rows")
    for rows in contiguous_rows:
        tops = True
        bots = True
        top_sides = 0
        bot_sides = 0
        for item in rows:
            row, col = item
            # check top and bottom. If contiguous top
            curr_top = (row - 1, col) in group_set
            curr_bot = (row + 1, col) in group_set
            # If previously not on a side and it is on a side,
            # we should add a side.
            if tops and not curr_top:
                top_sides += 1
            tops = curr_top
            if bots and not curr_bot:
                bot_sides += 1
            bots = curr_bot
        sides += top_sides + bot_sides
        print(rows, top_sides, bot_sides)
    print("cols")
    for cols in contiguous_columns:
        left = True
        right = True
        left_sides = 0
        right_sides = 0
        for item in cols:
            row, col = item
            curr_left = (row, col - 1) in group_set
            curr_right = (row, col + 1) in group_set
            if left and not curr_left:
                left_sides += 1
            left = curr_left
            if right and not curr_right:
                right_sides += 1
            right = curr_right
        sides += left_sides + right_sides
        print(cols, left_sides, right_sides)
    print(sides)
    return sides


def count_sides(groups: Dict[str, List[Tuple[int, int]]]) -> Dict[str, int]:
    results: Dict[str, int] = defaultdict(int)
    for id, group in groups.items():
        print(id)
        results[id] = process_group(group)
    return results


def part2(_input: InputType) -> int:
    area, perimeter, attribution = count_grid_area_perim(_input)
    groups = defaultdict(list)
    for (row, col, plot), attri in attribution.items():
        groups[attri].append((row, col))
    number_of_sides = count_sides(groups)
    total = 0
    for key in area:
        total += area[key] * number_of_sides[key]
    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
