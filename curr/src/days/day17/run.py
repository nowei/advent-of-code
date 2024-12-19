from typing import List, Tuple

InputType = Tuple[int, int, int, List[int]]
parent_path = "src/days/day17/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"

    with open(file_name, "r") as f:
        A = int(f.readline().strip().split(": ")[1])
        B = int(f.readline().strip().split(": ")[1])
        C = int(f.readline().strip().split(": ")[1])
        f.readline()
        program = [int(v) for v in f.readline().strip().split(": ")[1].split(",")]
    return A, B, C, program


class Game:
    A: int
    B: int
    C: int
    instruction: int
    program: List[int]
    output: List[int]
    debug: bool

    def __init__(self, A, B, C, program, debug=False):
        self.A = A
        self.B = B
        self.C = C
        self.instruction = 0
        self.program = program
        self.output = []
        self.debug = debug

    def _combo(self):
        val = self.program[self.instruction + 1]
        if val <= 3:
            return val
        elif val == 4:
            return self.A
        elif val == 5:
            return self.B
        elif val == 6:
            return self.C
        else:
            print("what")
            return -1

    def _literal(self):
        return self.program[self.instruction + 1]

    def adv(self):
        result = self.A // (2 ** self._combo())
        if self.debug:
            print(f"adv: A = {self.A} // ({2} ** {self._combo()}) = {result}")
        self.A = result
        self.instruction += 2

    def bxl(self):
        result = self.B ^ self._literal()

        if self.debug:
            print(f"bxl: B = {self.B} ^ ({self._literal()}) = {result}")
        self.B = result
        self.instruction += 2

    def bst(self):
        result = self._combo() % 8

        if self.debug:
            print(f"bst: B = {self._combo()} % ({8}) = {result}")
        self.B = result
        self.instruction += 2

    def jnz(self):
        final_instruction = self.instruction + 2 if self.A == 0 else self._literal()

        if self.debug:
            print(f"jnz: instruction is A={self.A} -> {final_instruction}")
        self.instruction = final_instruction

    def bxc(self):
        result = self.B ^ self.C

        if self.debug:
            print(f"bxc: B = {self.B} ^ ({self.C}) = {result}")
        self.B = result
        self.instruction += 2

    def out(self):
        self.output.append(self._combo() % 8)

        if self.debug:
            print(f"!!!out = {self._combo()} % ({8}) = {self.output[-1]}\n")
        self.instruction += 2

    def bdv(self):
        result = self.A // (2 ** self._combo())

        if self.debug:
            print(f"bdv: B = {self.A} // ({2} ** {self._combo()}) = {result}")
        self.B = result
        self.instruction += 2

    def cdv(self):
        result = self.A // (2 ** self._combo())

        if self.debug:
            print(f"cdv: C = {self.A} // ({2} ** {self._combo()}) = {result}")
        self.C = result
        self.instruction += 2

    def perform_op(self) -> bool:
        if self.instruction >= len(self.program):
            return False
        op = self.program[self.instruction]
        _val = self.program[self.instruction + 1]

        # if self.debug:
        #     print(" " + " " * (self.instruction * 3) + "v" + "--" + "v")
        #     print(self.program)
        #     print(f"A={self.A}, B={self.B}, C={self.C}")
        if op == 0:
            self.adv()
        elif op == 1:
            self.bxl()
        elif op == 2:
            self.bst()
        elif op == 3:
            self.jnz()
        elif op == 4:
            self.bxc()
        elif op == 5:
            self.out()
        elif op == 6:
            self.bdv()
        elif op == 7:
            self.cdv()
        return True


def _process(game: Game):
    while game.perform_op():
        pass
    return game.output


# 316674201
# 276560231
def part1(_input: InputType) -> str:
    A, B, C, program = _input
    game = Game(A, B, C, program, debug=False)
    _process(game)
    return ",".join(str(v) for v in game.output)


def part2(_input: InputType) -> str:
    A, B, C, program = _input
    print(program, len(program))
    # A = 593
    # arr = [3, 0, 3, 3, 0, 0, 1, 5, 9, 6, 0, 0, 0, 0, 0, 0]
    # dfs with this
    arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    res = [0, []]

    def search(arr, A, ind, matches):
        if ind >= len(arr):
            if matches > res[0]:
                res[0] = matches
                res[1] = list(arr)
                print(matches, res[0])
            if matches == len(arr):
                return True
            else:
                return False
        to_explore = []
        if ind > matches:
            # Note: Impossible to satisfy if the index we are trying is greater than matches ._.
            return False
        for i in range(10):
            arr[ind] = i
            cand = A + 8 ** (len(arr) - 1 - ind) * arr[ind]
            game = Game(cand, B, C, program, debug=False)
            _process(game)
            if len(program) != len(game.output):
                continue
            curr_matches = 0
            for j in range(len(program) - 1, -1, -1):
                if game.output[j] == program[j]:
                    curr_matches += 1
                else:
                    break
            to_explore.append((i, cand, curr_matches))
        for i, cand, curr_matches in sorted(to_explore, key=lambda x: (-x[-1], x[0])):
            arr[ind] = i
            if curr_matches < matches:
                print("Does this ever happen")
                continue
            print(arr, game.output, program, i, cand, curr_matches)
            if search(arr, cand, ind + 1, curr_matches):
                return True
        return False

    search(arr, 0, 0, 0)
    return ""


def test():
    g1 = Game(0, 0, 9, [2, 6])
    _process(g1)
    assert g1.B == 1
    g2 = Game(10, 0, 0, [5, 0, 5, 1, 5, 4])
    assert _process(g2) == "0,1,2"
    g3 = Game(2024, 0, 0, [0, 1, 5, 4, 3, 0])
    assert _process(g3) == "4,2,5,6,7,7,7,7,3,1,0"
    assert g3.A == 0
    g4 = Game(0, 29, 0, [1, 7])
    _process(g4)
    assert g4.B == 26
    g5 = Game(0, 2024, 43690, [4, 0])
    _process(g5)
    assert g5.B == 44354


def exec(part: int, execute: bool) -> str:
    _input = _parse_input(not execute)
    if part == 1:
        result = part1(_input)
    elif part == 2:
        result = part2(_input)
    elif part == 0:
        result = "0"
        test()
    return result
