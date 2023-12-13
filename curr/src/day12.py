from typing import Any, Optional, List
import argparse
import itertools

debug=False
debug=True

sample_file_path = "test/12.sample"
input_file_path = "test/12.input"

def fill_possibilities(s):
    for p in map(iter, itertools.product(".#", repeat=s.count('?'))):
        yield ''.join(c if c != '?' else next(p) for c in s)

class Record12:
    row: str
    reqs: List[int]

    def __init__(self, row: str, reqs: List[int]):
        self.row = row
        self.reqs = reqs

    def valid_permutations(self):
        # Note that we only care about the contiguous ? and #s
        # but for simplification, we try everything
        ans = 0
        for cand in fill_possibilities(self.row):
            checks = [len(v) for v in cand.split(".") if v != ""]
            if checks == self.reqs:
                print("ayo", cand)
                ans += 1
        return ans
    
    def bfs_permutations(self):
        cands = [[[v for v in self.row.split(".") if v != ""], self.reqs, ""]]
        count = 0
        # Cut to next ? or #
        while cands:
            curr, curr_reqs, locked = cands.pop()
            last_of_curr = curr.pop()
            for last_cand in fill_possibilities(last_of_curr):
                # print(last_cand)
                req_clone = curr_reqs.copy()
                vals = [len(v) for v in last_cand.split(".") if v != ""]
                failed = False
                while vals and req_clone:
                    if vals[-1] == req_clone[-1]:
                        req_clone.pop()
                        vals.pop()
                    else:
                        failed = True
                        break
                if not curr and not req_clone and not vals:
                    # print(last_cand + "." + locked)
                    count += 1
                    continue
                if vals and not req_clone:
                    continue
                # print(curr, req_clone, locked, "hello", failed, curr, req_clone)
                if not failed and curr:
                    curr_clone = curr.copy()
                    cands.append([curr_clone, req_clone, last_cand + "." + locked])

        # actual = self.valid_permutations() 
        # if actual != count:
        #     print(actual, count)
        #     print(self.row, self.reqs,)
        return count

    def dfs_permutations(self):
        print(self.row)
        char_array = [c for c in self.row]
        reqs = self.reqs.copy()

        def go_deep(curr, i, req_i, contiguous):
            if i == len(char_array):
                print(curr)
                if all(r == 0 for r in reqs):
                    return 1
                else:
                    return 0
            if char_array[i] == ".":
                if contiguous:
                    if reqs[req_i] != 0:
                        return 0
                    req_i += 1
                return go_deep(curr + ".", i + 1, req_i, contiguous=False)
            elif char_array[i] == "#":
                if reqs[req_i] == 0:
                    return 0
                reqs[req_i] -= 1
                res = go_deep(curr + "#", i + 1, req_i, contiguous=True)
                reqs[req_i] += 1
                return res
            else: # char_array[index] == "?"
                # Try both paths:
                p_res = 0
                if contiguous and reqs[req_i] == 0:
                    p_res = go_deep(curr + ".", i + 1, req_i + 1, contiguous=False)
                else:
                    p_res = go_deep(curr + ".", i + 1, req_i, contiguous=False)
                s_res = 0
                if reqs[req_i] != 0:
                    reqs[req_i] -= 1
                    s_res = go_deep(curr + "#", i + 1, req_i, contiguous=True)
                    reqs[req_i] -= 1
                return p_res + s_res
        result = go_deep("", 0, 0, False)

        actual = self.valid_permutations() 
        if actual != result:
            print(actual, result)
            print(self.row, self.reqs,)
        return result
class Springs12:
    records: List[Record12]

    def __init__(self, records):
        self.records = records
    
    def solve_summed(self) -> int:
        permutations = 0
        for record in self.records:
            permutations += record.dfs_permutations()
        return permutations

def parse_file_day12(file_path, example: str = "") -> Springs12:
    records = []
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    for line in lines:
        row, reqs_str = line.strip().split()
        reqs = [int(val) for val in reqs_str.split(",")]
        record = Record12(row, reqs)
        records.append(record)
    return Springs12(records)

def solve_day12_part1(input: Springs12) -> int:
    return input.solve_summed()

def solve_day12_part2(input: Springs12) -> int:
    return 0
    return input.solve_summed()

def solve_day12(input: Springs12, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None):
    out_part1 = solve_day12_part1(input)

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

    # copied input with ? joins
    records = []
    for s in input.records:
        record = Record12("?".join([s.row for _ in range(5)]), s.reqs * 5)
        records.append(record)
    input = Springs12(records)

    out_part2 = solve_day12_part2(input)
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

def main_12(run_all: bool = False, example: Optional[str] = None):
    if example:
        print("Testing input from cmd line")
        input = parse_file_day12("", example=example)
        solve_day12(input)
        exit(0)
    print("Running script for day 12")
    print("Sample input")
    expected_out_part1 = 21
    expected_out_part2 = 525152
    print("---------------------------------")
    print("Input file:", sample_file_path)
    input = parse_file_day12(sample_file_path)
    solve_day12(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)
    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day12(input_file_path)
        solve_day12(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    parser.add_argument("-e", '--example')
    args = parser.parse_args()
    main_12(run_all=args.actual, example=args.example)
