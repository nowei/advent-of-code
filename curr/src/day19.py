from typing import Any, Optional, List, Dict, Callable, Tuple
from collections import defaultdict
import argparse

sample_file_path = "test/19.sample"
input_file_path = "test/19.input"

class Rule19:
    var: str
    comp: str
    i: int
    result: str

    def __init__(self, var, comp, i, result):
        self.var = var
        self.comp = comp
        self.i = i
        self.result = result
    
    def process(self, part: Dict[str, int]) -> str:
        if self.comp == ">":
            if part[self.var] > self.i:
                return self.result
            else:
                return ""
        elif self.comp == "<": 
            if part[self.var] < self.i:
                return self.result
            else:
                return ""
        else:
            return self.result
    
    def process_splits(self, cand: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
        if not self.comp:
            return [], cand
        result = [c for c in cand]
        ind = {"x":0, "m":1, "a": 2, "s": 3}[self.var]
        c_min, c_max = cand[ind]
        # all sats self.i < |-----------------|
        # split    |---------------->----------|
        # no sats  > |----------|
        if self.comp == ">":  # [c_min, c_max] > self.i
            if c_min > self.i: # all sats
                return [], result
            elif c_max <= self.i:
                return cand, []
            else:
                cand[ind] = (c_min, self.i)
                result[ind] = (self.i + 1, c_max)
                return cand, result
        else: # self.comp == "<"
            if c_max < self.i:
                return [], result
            elif c_min >= self.i:
                return cand, []
            else:
                cand[ind] = (self.i, c_max)
                result[ind] = (c_min, self.i - 1)
                return cand, result
    def __repr__(self):
        return f"({self.var} {self.comp} {self.i}: {self.result})"

class Rules19:
    steps: List[Rule19]

    def __init__(self, steps):
        self.steps = steps

    def process(self, part: Dict[str, int]):
        for f in self.steps:
            res = f.process(part)
            if res != "":
                return res
        return ""

def process_rules(rules_str: str) -> List[Callable[[Dict[str, int]], str]]:
    funcs = []
    for rule in rules_str:
        if ":" in rule:
            cond, res = rule.split(":")
            if "<" in cond:
                var, num = cond.split("<")
                v = Rule19(var, "<", int(num), res)
            else:
                var, num = cond.split(">")
                v = Rule19(var, ">", int(num), res)
        else:
            v = Rule19("", "", 0, rule)
        funcs.append(v)
    return funcs

class Setting19:
    rules: Dict[str, Rules19]
    parts: List[Dict[str, int]]

    def __init__(self, rules, parts):
        self.rules = rules
        self.parts = parts
    
    def process(self) -> int:
        total = 0
        for p in self.parts:
            res = "in"
            while not (res == "A" or res == "R"):
                res = self.rules[res].process(p)
            if res == "A":
                total += p["x"] + p["m"] + p["a"] + p["s"]
        return total

    def process_splits(self) -> int:
        total = 0
        cands = {"in": [[(1, 4000), (1, 4000), (1, 4000), (1, 4000)]]}
        while cands:
            next_cands = defaultdict(lambda: list())
            for k in cands:
                rule = self.rules[k]
                for curr in cands[k]:
                    print(k, curr)
                    for r in rule.steps:
                        curr, resulting = r.process_splits(curr)
                        print(r, curr, resulting)
                        if resulting:
                            next_cands[r.result].append(resulting)
                        else:
                            if not curr:
                                break
                            next_cands[r.result].append(curr)
                    print()
            if "A" in next_cands:
                for a, b, c, d in next_cands["A"]:
                    # The +1 is for the inclusive range 
                    total += (a[1] - a[0] + 1) * (b[1] - b[0] + 1) * (c[1] - c[0] + 1) * (d[1] - d[0] + 1)
                next_cands.pop("A")
            if "R" in next_cands:
                next_cands.pop("R")
            cands = next_cands
        return total

def parse_file_day19(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    parts = []
    rules = {}
    parts_flag = False
    for line in lines:
        stripped = line.strip()
        if stripped == "":
            parts_flag = True
            continue
        if not parts_flag:
            name, rule_set = stripped.split("{")
            rules[name] = Rules19(process_rules(rule_set.strip("}").split(",")))
        else:
            x, m, a, s = [int(v.split("=")[1]) for v in stripped.strip("{}").split(",")]
            parts.append({"x": x, "m": m, "a": a, "s": s})
    return Setting19(rules, parts)

def solve_day19_part1(input: Setting19) -> int:
    return input.process()

def solve_day19_part2(input: Setting19) -> int:
    return input.process_splits()

def solve_day19(input: Setting19, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None):
    out_part1 = solve_day19_part1(input)

    if expected_pt1 is not None:
        if out_part1 != expected_pt1:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_pt1)
        else:
            print("Sample matched")
    print("Part 1 result:")
    print(out_part1)
    print()

    out_part2 = solve_day19_part2(input)
    if expected_pt2 is not None:
        if out_part2 != expected_pt2:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_pt2)
        else:
            print("Sample matched")
    print("Part 2 result:")
    print(out_part2)
    print()

def main_19(run_all: bool = False, example: Optional[str] = None):
    if example:
        print("Testing input from cmd line")
        input = parse_file_day19("", example=example)
        solve_day19(input)
        exit(0)

    print("Running script for day 19")
    print("Sample input")
    print("---------------------------------")
    expected_out_part1 = 19114
    expected_out_part2 = 167409079868000
    print("Input file:", sample_file_path)
    input = parse_file_day19(sample_file_path)
    solve_day19(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day19(input_file_path)
        solve_day19(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    args = parser.parse_args()
    main_19(run_all=args.actual)
