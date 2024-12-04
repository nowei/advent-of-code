from collections import defaultdict
from typing import Any, Optional, List, NamedTuple, Dict, Tuple
import argparse
from enum import Enum

sample_file_path = "test/20.sample"
sample_2_file_path = "test/20.sample2"
input_file_path = "test/20.input"


class Energy20(Enum):
    LOW = 0
    HIGH = 1


class Packet20(NamedTuple):
    sender: str
    energy: Energy20


class Module20:
    name: str
    destinations: List[str]
    state: bool

    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations
        self.state = False

    def receive(self, packet: Packet20) -> Optional[Packet20]:
        pass

    def process(self, packet: Packet20) -> List[Tuple[str, Packet20]]:
        res = self.receive(packet)
        if res is None:
            return []
        return [(dest, res) for dest in self.destinations]

    def reset(self):
        pass


class FlipFlop20(Module20):
    state: bool

    def __init__(self, name, destinations):
        super().__init__(name, destinations)
        self.state = False

    def receive(self, packet: Packet20) -> Optional[Packet20]:
        if packet.energy == Energy20.HIGH:
            return None
        # energy == Energy20.LOW
        if self.state:
            ret = Energy20.LOW
        else:
            ret = Energy20.HIGH
        self.state = not self.state
        return Packet20(self.name, ret)

    def __repr__(self):
        return f"{self.name}:ff({self.state})"

    def reset(self):
        self.state = False


class Conjunction20(Module20):
    inputs: Dict[str, Energy20]

    def __init__(self, name, destinations, inputs):
        super().__init__(name, destinations)
        self.inputs = {}
        for i in inputs:
            self.inputs[i] = Energy20.LOW

    def receive(self, packet: Packet20) -> Optional[Packet20]:
        self.inputs[packet.sender] = packet.energy
        if all([self.inputs[m] == Energy20.HIGH for m in self.inputs]):
            return Packet20(self.name, Energy20.LOW)
        else:
            return Packet20(self.name, Energy20.HIGH)

    def __repr__(self):
        conj_str = ",".join([str(self.inputs[k]) for k in sorted(self.inputs.keys())])
        return f"{self.name}:conj({conj_str})"

    def reset(self):
        self.inputs = {k: Energy20.LOW for k in self.inputs}


class Broadcast20(Module20):
    def __init__(self, name, destinations):
        super().__init__(name, destinations)

    def receive(self, packet: Packet20) -> Optional[Packet20]:
        return Packet20(self.name, packet.energy)

    def __repr__(self):
        return "broadcast"


class Setting20:
    mods: Dict[str, Module20]
    from_map: Dict[str, List[str]]

    def __init__(self, mods: Dict[str, Module20], from_map: Dict[str, List[str]]):
        self.mods = mods
        self.from_map = from_map

    def press(
        self, cond: Optional[Tuple[str, Energy20]] = None, debug: bool = False
    ) -> (List[Tuple[int, int]], bool):
        packets = [("broadcaster", Packet20("button", Energy20.LOW))]
        packet_hash = []
        found = False

        if debug:
            print("start", self)
        while packets:
            if debug:
                print(packets)
            new_packets = []
            num_low = 0
            num_high = 0
            for dest, packet in packets:
                if packet.energy == Energy20.LOW:
                    num_low += 1
                elif packet.energy == Energy20.HIGH:
                    num_high += 1
                res = []
                if dest in self.mods:
                    res = self.mods[dest].process(packet)
                if cond and dest == cond[0] and cond[1] == packet.energy:
                    found = True
                new_packets.extend(res)
            packet_hash.append((num_low, num_high))
            packets = new_packets
        if debug:
            print("end", self)
        packet_hash.append(hash(str(self)))
        return packet_hash, found

    def __repr__(self):
        return ";".join(str(self.mods[k]) for k in sorted(self.mods.keys()))

    def reset(self):
        for k in self.mods:
            self.mods[k].reset()

    def press_until(self, cond: Tuple[str, Energy20]) -> int:
        num_presses = 0
        print(cond)
        found = False
        while not found:
            _, found = self.press(cond=cond, debug=False)
            num_presses += 1
        return num_presses

    def process_until_rx(self):
        # analyze cycles from rx
        prev = self.from_map["rx"][0]
        indiv_results = self.from_map[prev]
        # reconstruct results into cycles, look until some condition is true
        subgraphs = {}
        num_presses = 1
        for p in indiv_results:
            # keep walking self.from_map until we no longer see results
            seen = set()
            curr_cycle = [p]
            while curr_cycle:
                for prev in self.from_map[curr_cycle.pop()]:
                    if prev not in seen:
                        seen.add(prev)
                        curr_cycle.append(prev)
            seen.add(p)
            subgraphs[p] = Setting20(
                {k: self.mods[k] for k in seen}, {k: self.from_map[k] for k in seen}
            )
            # need to determine when each subgraph is high
            # check that `p` gets a high signal
            num_presses *= subgraphs[p].press_until(("dt", Energy20.HIGH))

        return num_presses

    def process_simple(self, num_presses=1000):
        low_presses = 0
        high_presses = 0
        for _ in range(num_presses):
            layer, _ = self.press()
            for low, high in layer[:-1]:
                low_presses += low
                high_presses += high
        return low_presses * high_presses

    def process(self, num_presses=1000):
        layers = []
        seen = set()
        # find the pattern for how many times things trip over before it starts to repeat
        # kind of like hashing outputs
        curr = None
        while curr not in seen:
            if curr:
                layers.append(curr)
                seen.add(curr)
            curr = tuple(self.press())
        print(layers)
        print(curr)
        last_curr = curr
        cycle_start = layers.index(last_curr)
        # already_pressed = len(layers)
        cycle_length = len(layers[cycle_start:])
        remaining_presses = num_presses - cycle_start
        remaining_cycles, remaining_cycle_presses = divmod(
            remaining_presses, cycle_length
        )
        low_presses = 0
        high_presses = 0
        # To get to where it starts to cycle
        for layer in layers[:cycle_start]:
            for low, high in layer[:-1]:
                low_presses += low
                high_presses += high
        cycle_presses = []
        cycle_low = 0
        cycle_high = 0
        for layer in layers[cycle_start:]:
            layer_low = 0
            layer_high = 0
            for low, high in layer[:-1]:
                layer_low += low
                layer_high += high
            cycle_presses.append((layer_low, layer_high))
            cycle_low += layer_low
            cycle_high += layer_high
        low_presses += cycle_low * remaining_cycles
        high_presses += cycle_high * remaining_cycles
        for i in range(remaining_cycle_presses):
            low_presses += cycle_presses[i][0]
            high_presses += cycle_presses[i][1]
        return low_presses * high_presses


def parse_file_day20(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    from_map = defaultdict(lambda: list())
    mods = {}
    conjunct = []
    for line in lines:
        curr, destinations_str = line.strip().split(" -> ")
        destinations = destinations_str.split(", ")
        if curr == "broadcaster":
            name = curr
            m = Broadcast20(name, destinations)
            mods[name] = m
        else:
            name = curr[1:]
            if "%" in curr:
                m = FlipFlop20(name, destinations)
                mods[name] = m
            elif "&" in curr:
                conjunct.append([name, destinations])
        for dest in destinations:
            from_map[dest].append(name)
    for name, destinations in conjunct:
        mods[name] = Conjunction20(name, destinations, from_map[name])

    return Setting20(mods, from_map)


def solve_day20_part1(input: Setting20) -> int:
    return input.process_simple()


def solve_day20_part2(input: Setting20) -> int:
    return input.process_until_rx()


def solve_day20(
    input: Setting20,
    expected_pt1: Optional[int] = None,
    expected_pt2: Optional[int] = None,
    only_pt1: bool = False,
):
    out_part1 = solve_day20_part1(input)

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
    input.reset()

    if not only_pt1:
        out_part2 = solve_day20_part2(input)
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


def main_20(run_all: bool = False, example: Optional[str] = None):
    if example:
        print("Testing input from cmd line")
        input = parse_file_day20("", example=example)
        solve_day20(input)
        exit(0)

    print("Running script for day 20")
    print("Sample input")
    print("---------------------------------")
    expected_out_part1 = 32000000
    expected_out_part2 = None
    print("Input file:", sample_file_path)
    input = parse_file_day20(sample_file_path)
    solve_day20(
        input,
        expected_pt1=expected_out_part1,
        expected_pt2=expected_out_part2,
        only_pt1=True,
    )
    input = parse_file_day20(sample_2_file_path)
    solve_day20(input, expected_pt1=11687500, only_pt1=True)

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day20(input_file_path)
        solve_day20(input)
        # p1: 442000000 too low
        # p2: 711650489 too low


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--actual", action="store_true")
    args = parser.parse_args()
    main_20(run_all=args.actual)
