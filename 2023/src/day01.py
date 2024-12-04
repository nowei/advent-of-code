from typing import List, Dict, Optional

sample_file_path = "test/01.sample"
sample_part2_file_path = "test/01.sample2"
input_file_path = "test/01.input"

expected_out_part1 = 142
expected_out_part2 = 281

def parse_file_day01(file_path) -> List[str]:
    input = []
    with open(file_path, "r") as f:
        for line in f:
            input.append(line.strip())
    return input

def solve_day01_part1(input: List[str]) -> int:
    answer = 0
    for line in input:
        first_digit = None
        second_digit = None
        for c in line:
            if c.isdigit():
                first_digit = int(c)
                break
        for c in line[::-1]:
            if c.isdigit():
                second_digit = int(c)
                break
        answer += first_digit * 10 + second_digit
    return answer



class Trie():
    value: Optional[int]
    children: Dict[str, "Trie"]
    terminal: bool = False

    def __init__(self):
        self.value = None
        self.children = {}
        self.terminal = False
    
    def __repr__(self):
        inside = ""
        if self.children:
            inside += "children={};".format(self.children.keys())
        if self.terminal:
            inside += "value={}".format(self.value)
        return "Trie({})".format(inside)

    def __str__(self):
        return "member of Trie"

def build_trie(values: Dict[str, int]) -> Trie:
    start = Trie()
    for word in values:
        ptr = start
        for i in range(len(word)):
            c = word[i]
            if c not in ptr.children:
                ptr.children[c] = Trie()
            ptr = ptr.children[c]
            if i == len(word) - 1:
                ptr.terminal = True
                ptr.value = values[word]
    return start

digit_strs = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
forward_trie = build_trie(digit_strs)
backward_trie = build_trie({s[::-1]: digit_strs[s] for s in digit_strs})

def check_trie(line: str, i: int, trie: Trie) -> Optional[int]:
    ptr = trie
    while i < len(line) and line[i] in ptr.children:
        ptr = ptr.children[line[i]]
        i += 1
    if ptr.terminal:
        return ptr.value

    return None
    
def solve_day01_part2(input: List[str]) -> int:
    answer = 0
    for line in input:
        first_digit = None
        second_digit = None
        # we check the forward string and break
        # and the backwards string and break
        # forward check
        for i in range(len(line)):
            if line[i].isdigit():
                first_digit = int(line[i])
                break
            else:
                out = check_trie(line, i, forward_trie)
                if out is not None:
                    first_digit = out
                    break
        reversed_line = line[::-1]
        for i in range(len(reversed_line)):
            if reversed_line[i].isdigit():
                second_digit = int(reversed_line[i])
                break
            else:
                out = check_trie(reversed_line, i, backward_trie)
                if out is not None:
                    second_digit = out
                    break
        answer += first_digit * 10 + second_digit
    return answer

def solve_day01(file_path: str, check_out: bool = False):
    input = parse_file_day01(file_path)
    out_part1 = solve_day01_part1(input)

    if check_out:
        if out_part1 != expected_out_part1:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_out_part1)
        else:
            print("Sample matched")
    print("Part 1 result:")
    print(out_part1)

    if "sample" in file_path:
        input = parse_file_day01(sample_part2_file_path)
    out_part2 = solve_day01_part2(input)
    if check_out:
        if out_part2 != expected_out_part2:
            print("Sample results do not match")
            print("Sample expected:")
            print(expected_out_part2)
        else:
            print("Sample matched")
    print("Part 2 result:")
    print(out_part2)
    print()

def main_01(only_sample: bool = False):
    print("Running script for day 01")
    solve_day01(sample_file_path, check_out=True)
    if not only_sample:
        solve_day01(input_file_path, check_out=False)
    


if __name__ == "__main__":
    main_01(only_sample=False)