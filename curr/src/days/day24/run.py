from typing import Dict, Tuple, List
from collections import defaultdict

InputType = Tuple[Dict[str, int], Dict[str, Dict[str, Dict[str, List[str]]]]]
parent_path = "src/days/day24/"


def _parse_input(sample: bool) -> InputType:
    # file_name = parent_path + "input.txt"
    file_name = parent_path + "input2.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    initial_values = {}
    equations: Dict[str, Dict[str, Dict[str, List[str]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))
    )
    eqs = False
    with open(file_name, "r") as f:
        for line in f:
            if line == "\n":
                eqs = True
                continue
            if eqs:
                left, c = line.strip().split(" -> ")
                a, op, b = left.split(" ")
                equations[a][b][op].append(c)
                equations[b][a][op].append(c)
            else:
                a, val = line.strip().split(": ")
                initial_values[a] = int(val)
    return initial_values, equations


def evaluate_dag(
    values: Dict[str, int],
    equations: Dict[str, Dict[str, Dict[str, List[str]]]],
) -> Dict[str, int]:
    can_be_evaluated = set()
    seen = set()
    # initial pass to see what equations can be evaluated
    for a in equations:
        for b in equations[a]:
            if a in values and b in values:
                can_be_evaluated.add((min(a, b), max(a, b)))
    while can_be_evaluated:
        new_layer = set()
        added = set()
        for a, b in can_be_evaluated:
            seen.add((a, b))
            for op in equations[a][b]:
                cs = equations[a][b][op]
                val = 0
                if op == "AND":
                    val = values[a] & values[b]
                elif op == "XOR":
                    val = values[a] ^ values[b]
                elif op == "OR":
                    val = values[a] | values[b]
                for c in cs:
                    added.add(c)
                    values[c] = val
        for a in added:
            for b in equations[a]:
                if a in values and b in values:
                    new_layer.add((min(a, b), max(a, b)))
        can_be_evaluated = new_layer
    return values


def part1(_input: InputType) -> int:
    values, equations = _input
    final_values = evaluate_dag(values, equations)
    final_bytes = ""
    for k in sorted(final_values):
        if not k.startswith("z"):
            continue
        final_bytes += str(final_values[k])
    print(final_bytes)

    return int(final_bytes[::-1], 2)


def _trace_equations(equations: Dict[str, Dict[str, Dict[str, List[str]]]]):
    eqs: Dict[str, Tuple[str, str, str, str]] = {}
    for a in equations:
        for b in equations[a]:
            for op in equations[a][b]:
                for c in equations[a][b][op]:
                    eqs[c] = (min(a, b), op, max(a, b), c)
    zs = []
    for c in sorted(eqs):
        if c.startswith("z"):
            zs.append(c)
    for z in zs:
        relevants = []
        relevants.append(eqs[z])
        relevants_idx = 0
        seen = set()
        while relevants_idx < len(relevants):
            a, op, b, _c = relevants[relevants_idx]
            if a in eqs and eqs[a] not in seen:
                relevants.append(eqs[a])
                seen.add(eqs[a])
            if b in eqs and eqs[b] not in seen:
                relevants.append(eqs[b])
                seen.add(eqs[b])
            relevants_idx += 1
        xs_seen = []
        ys_seen = []
        for trip in relevants[::-1]:
            print(" ".join(trip[0:3]) + " = " + trip[3])
            if trip[0].startswith("x"):
                xs_seen.append(trip[0])
            if trip[2].startswith("y"):
                ys_seen.append(trip[2])
        a, op, b, c = relevants[0]
        current_equation = [a, op, b, "=", c]
        for relevant in relevants[1:]:
            a, op, b, c = relevant
            for i in range(len(current_equation)):
                if current_equation[i] == c:
                    current_equation = (
                        current_equation[0:i]
                        # + ["(", a, op, b, "=", c, ")"]
                        + ["(", a, op, b, ")"]
                        + current_equation[i + 1 :]
                    )
                    break
        print(" ".join(current_equation).replace("( ", "(").replace(" )", ")"))
        print(z)
        print(xs_seen)
        print(ys_seen)
        print()
        should_see = set(range(int(z[1:])))
        for i in range(len(xs_seen)):
            assert xs_seen[i][1:] == ys_seen[i][1:]
            x_val = int(xs_seen[i][1:])
            if x_val in should_see:
                should_see.remove(x_val)
        print(should_see)


def part2(_input: InputType) -> str:
    values, equations = _input
    x = ""
    y = ""
    for k in sorted(values):
        if k.startswith("x"):
            x += str(values[k])
        else:  # k.startswith("y")
            y += str(values[k])
    # ckb,kbs,ksv,nbd,tqq,z06,z20,z39
    swaps = [
        # Fix 6?
        # x06 AND y06 = z06
        # qtf XOR nsp = ksv
        [("x06", "y06", "AND", "z06"), ("nsp", "qtf", "XOR", "ksv")],
        # Fix 10?
        # x10 AND y10 = nbd
        # y10 XOR x10 -> kbs
        [("x10", "y10", "AND", "nbd"), ("x10", "y10", "XOR", "kbs")],
        # Fix 20?
        # dnc OR tsm = z20
        # bnp XOR mtq = tqq
        [("dnc", "tsm", "OR", "z20"), ("bnp", "mtq", "XOR", "tqq")],
        # Fix 39?
        # cmj AND hpp = z39
        # cmj XOR hpp = ckb
        [("cmj", "hpp", "AND", "z39"), ("cmj", "hpp", "XOR", "ckb")],
    ]
    swapped_keys = []
    for (a, b, op1, c), (d, e, op2, f) in swaps:
        equations[a][b][op1] = [f]
        equations[b][a][op1] = [f]
        equations[d][e][op2] = [c]
        equations[e][d][op2] = [c]
        swapped_keys.append(f)
        swapped_keys.append(c)

    x = x[::-1]
    y = y[::-1]
    int_x, int_y = int(x, 2), int(y, 2)
    print()
    print("x = ", x, "=", int_x)
    print("y = ", y, "=", int_y)
    print("z =", str(bin(int_x + int_y))[2:], "=", int_x + int_y)
    print()
    traced = _trace_equations(equations)
    final_values = evaluate_dag(values, equations)
    final_bytes = ""
    for k in sorted(final_values):
        if not k.startswith("z"):
            continue
        final_bytes += str(final_values[k])
    print("actual: ", str(bin(int_x + int_y))[2:])
    print("current:", final_bytes[::-1])

    print(bin(int(final_bytes[::-1], 2) ^ (int_x + int_y)))
    print(int(final_bytes[::-1], 2))
    return ",".join(list(sorted(swapped_keys)))


def exec(part: int, execute: bool) -> int | str:
    _input = _parse_input(not execute)
    result: int | str
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
