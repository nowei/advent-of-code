from typing import List, Tuple, Dict
from pydantic import BaseModel
from z3 import Int, Optimize, sat, Sum


class Setting(BaseModel):
    target: Tuple[bool, ...]
    levers: List[Tuple[int, ...]]
    joltages: Tuple[int, ...]


InputType = List[Setting]
parent_path = "src/days/day10/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    settings = []
    with open(file_name, "r") as f:
        for line in f:
            target = tuple((True,))
            levers: List[Tuple[int, ...]] = []
            joltages = tuple((1,))
            for block in line.strip().split():
                if block.startswith("["):
                    target = tuple(
                        [True if v == "#" else False for v in block.strip("[]")]
                    )
                elif block.startswith("("):
                    levers.append(tuple([int(v) for v in block.strip("()").split(",")]))
                elif block.startswith("{"):
                    joltages = tuple([int(v) for v in block.strip("{}").split(",")])
            settings.append(Setting(target=target, levers=levers, joltages=joltages))

    return settings


def part1(_input: InputType) -> int:
    # Dijkstra's to target path?
    from collections import deque

    # Same as BFS because the cost of making one move is 1...
    def dijkstras(goal, moves):
        print(goal, moves)
        initial = tuple([False for _ in range(len(goal))])
        layers = deque([(initial, m, 1) for m in moves])
        tracer: Dict[
            Tuple[bool, ...], Tuple[Tuple[bool, ...], Tuple[int, ...], int]
        ] = {initial: (initial, tuple(()), 0)}
        while layers:
            curr_layout, move, level = layers.popleft()
            # apply current lever to board
            output = tuple(
                [
                    curr_layout[i] if i not in move else not curr_layout[i]
                    for i in range(len(curr_layout))
                ]
            )
            if output == goal:
                return level
            if output in tracer:
                continue
            tracer[output] = (curr_layout, move, level)
            for next_moves in moves:
                layers.append((output, next_moves, level + 1))

    outputs = []
    for setting in _input:
        goal = setting.target
        outputs.append(dijkstras(goal, setting.levers))
    print(outputs)
    return sum(outputs)


def part2(_input: InputType) -> int:
    import heapq

    def dijkstras(goal, moves):  # too slow... with heuristic
        print(goal, moves)
        new_goal = tuple([0] * len(goal))
        moves = sorted(moves, key=lambda x: -len(x))
        print("moves", moves)
        moves = [[-1 if i in move else 0 for i in range(len(goal))] for move in moves]
        print("translated moves", moves)
        # Assume every state is valid
        layers = [(sum(goal), 1, sum(goal), goal)]
        tracer: Dict[Tuple[int, ...], Tuple[Tuple[int, ...], int]] = {}
        while layers:
            cost, level, distance, curr_layout = heapq.heappop(layers)
            # print(distance, curr_layout, level)
            tracer[curr_layout] = (goal, sum(goal))
            # print("eval", distance, level, curr_layout)
            # apply current lever to board
            print(cost, level, distance, curr_layout, len(layers))
            considerations = []
            for move in moves:
                curr = curr_layout
                curr_level = level
                while all(curr[i] >= 0 for i in range(len(curr_layout))):
                    curr = tuple(map(sum, zip(curr, move)))
                    if any(curr[i] < 0 for i in range(len(curr_layout))):
                        break
                    if curr in tracer:
                        curr_level += 1
                        continue
                    if curr == new_goal:
                        # print(curr_level, curr_level, curr, new_goal)
                        return curr_level
                    curr_level += 1
                    considerations.append((curr, curr_level))
            # print(considerations)
            for output in considerations:
                next_layout, levels_to_get_here = output
                if next_layout in tracer:
                    continue
                tracer[next_layout] = (curr_layout, levels_to_get_here)
                heapq.heappush(
                    layers,
                    (
                        levels_to_get_here * sum(next_layout),
                        levels_to_get_here,
                        sum(next_layout),
                        next_layout,
                    ),
                )
        return 0

    def f_math(goal, moves):
        from collections import defaultdict

        vars = [Int("v%d" % i) for i in range(len(moves))]
        s = Optimize()
        for v in vars:
            s.add(v >= 0)
        related_indicies = defaultdict(list)
        for i in range(len(moves)):
            move = moves[i]
            for trigger in move:
                related_indicies[trigger].append(i)
        print(related_indicies)
        for i in range(len(goal)):
            triggers = related_indicies[i]
            s.add(sum(vars[trigger] for trigger in triggers) == goal[i])
        objective = Sum(vars)
        s.minimize(objective)
        print(s.check() == sat)
        model = s.model()
        return sum(int(str(model[var])) for var in vars)

    outputs = []
    for setting in _input:
        goal = setting.joltages
        outputs.append(f_math(goal, setting.levers))
    print(outputs)
    return sum(outputs)


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
