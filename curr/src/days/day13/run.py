from typing import List, Tuple
from itertools import islice


class Button:
    x: int
    y: int
    cost: int

    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost


InputType = List[Tuple[List[int], Button, Button]]
parent_path = "src/days/day13/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    games = []
    with open(file_name, "r") as f:
        while True:
            lines_gen = islice(f, 4)
            btnA = next(lines_gen)
            btnB = next(lines_gen)
            target = next(lines_gen)
            a_x, a_y = [
                int(v.split("+")[1]) for v in btnA.strip().split(": ")[1].split(", ")
            ]
            b_x, b_y = [
                int(v.split("+")[1]) for v in btnB.strip().split(": ")[1].split(", ")
            ]
            x, y = [
                int(v.split("=")[1]) for v in target.strip().split(": ")[1].split(", ")
            ]
            games.append(([x, y], Button(a_x, a_y, 3), Button(b_x, b_y, 1)))
            if not next(lines_gen, None):
                break
    return games


def _play_game_iterative(
    target: List[int], btnA: Button, btnB: Button, max_presses: int = 100, id: int = 0
):
    target_x, target_y = target
    for i in range(max_presses, -1, -1):
        curr_x = target_x - i * btnB.x
        curr_y = target_y - i * btnB.y
        if curr_x < 0 or curr_y < 0:
            continue
        m_x, r_x = divmod(curr_x, btnA.x)
        m_y, r_y = divmod(curr_y, btnA.y)
        if r_x == 0 and r_y == 0 and m_x == m_y:
            print(id, m_x, i)
            return i * btnB.cost + m_x * btnA.cost
    return 0


def part1(_input: InputType) -> int:
    total = 0
    for i, (target, btnA, btnB) in enumerate(_input):
        total += do_some_math(target, btnA, btnB, id=i)
        # total += _play_game_iterative(target, btnA, btnB, id=i)
    return total


def _play_game(
    target: List[int],
    btnA: Button,
    btnB: Button,
    max_presses: int,
):
    # Some kind of binary search
    best_cost = float("inf")
    # Start with btnB pressing 50 times
    b_low = 0
    b_high = max_presses
    target_x, target_y = target
    print(target)
    while b_low <= b_high:
        b_mid = (b_high + b_low) // 2
        curr_x = target_x - b_mid * btnB.x
        curr_y = target_y - b_mid * btnB.y
        print(f"B({b_mid}): low({b_low}), high({b_high}), {curr_x}, {curr_y}")
        if curr_x < 0 or curr_y < 0:
            b_high = b_mid - 1
            continue
        m_x, r_x = divmod(curr_x, btnA.x)
        m_y, r_y = divmod(curr_y, btnA.y)
        print("A", m_x, m_y, r_x, r_y)
        if m_x > max_presses or m_y > max_presses:
            # Need to press B more times
            b_low = b_mid + 1
            continue
        if m_x == m_y and r_x == 0 and r_y == 0:
            cost = b_mid * btnB.cost + m_x * btnA.cost
            if cost < best_cost:
                best_cost = cost
            # found, we can be more greedy and try to increase the lower bound
            b_low = b_mid + 1
            continue
        cand_x = curr_x - max(m_x, m_y) * btnA.x
        cand_y = curr_y - max(m_x, m_y) * btnA.y
        if cand_x < 0 or cand_y < 0:
            # still to high
            b_high = b_mid - 1
            continue

        b_low = b_mid + 1
    print(best_cost)
    if best_cost == float("inf"):
        return 0
    return best_cost


def do_some_math(target: List[int], btnA: Button, btnB: Button, id: int = 0):
    # (a_x * a_c) + (b_x * b_c) = t_x
    # (a_y * a_c) + (b_y * b_c) = t_y
    # minimize a_c * 3 + b_c
    # b_c = (t_x - a_x * a_c) / b_x
    # (a_y * a_c) + b_y * (b_c) = t_y
    # (a_y * a_c) + b_y * (t_x - a_x * a_c) / b_x = t_y
    # (a_y * a_c) + (b_y * t_x / b_x) -  a_c * (b_y * a_x / b_x) = t_y
    # a_c * (a_y - b_y * a_x / b_x) = t_y - (b_y * t_x / b_x)
    # a_c = (t_y - (b_y * t_x / b_x)) / (a_y - b_y * a_x / b_x)
    t_x, t_y = target
    a_x, a_y = btnA.x, btnA.y
    b_x, b_y = btnB.x, btnB.y
    a_c = round((t_y - (b_y * t_x / b_x)) / (a_y - b_y * a_x / b_x))
    b_c = round((t_x - a_x * a_c) / b_x)
    if not (a_x * a_c) + (b_x * b_c) == t_x or not (a_y * a_c) + (b_y * b_c) == t_y:
        return 0
    a_c = int(a_c)
    b_c = int(b_c)
    # Note: Upon review, there is only one solution lmao
    # I got baited by this: https://en.wikipedia.org/wiki/Diophantine_equation#:~:text=In%20mathematics%2C%20a%20Diophantine%20equation,integer%20solutions%20are%20of%20interest.
    # https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity
    # But there are two equations, so the solution is unique.
    # gcd_x = math.gcd(a_x, b_x)
    # gcd_y = math.gcd(a_y, b_y)
    # if gcd_x != gcd_y:
    print(id, a_c, b_c)
    return a_c * btnA.cost + b_c * btnB.cost
    # # solutions will be in the form of
    # # x = x_1 - r b / gcd(a, b)
    # a_c_1 = a_c
    # b_c_1 = b_c
    # best_a_c = a_c
    # best_b_c = b_c
    # for i in range(10):
    #     n_a_c = a_c_1 - i * a_x // gcd_x
    #     n_b_c = b_c_1 + i * b_x // gcd_y
    #     if n_a_c >= 0 and n_b_c <= 100:
    #         best_a_c = n_a_c
    #         best_b_c = n_b_c
    #     else:
    #         break
    # print(id, best_a_c, best_b_c)
    # return best_a_c * btnA.cost + best_b_c * btnB.cost


def part2(_input: InputType) -> int:
    total = 0
    for i, (target, btnA, btnB) in enumerate(_input):
        target = [t + 10000000000000 for t in target]
        total += do_some_math(target, btnA, btnB, id=i)
    return total


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
