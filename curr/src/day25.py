from typing import Any, Optional, List, Tuple, Dict, Set
import argparse
from collections import defaultdict
import random
import networkx as nx

sample_file_path = "test/25.sample"
input_file_path = "test/25.input"

class Setting25:
    wires: Dict[str, Set[str]]
    edges: Set[Tuple[str, str]]
    vertices: Set[str]

    def __init__(self, wires, edges, vertices):
        self.wires = wires
        self.edges = edges
        self.vertices = vertices

class Community:
    id: int
    nodes: Set[str]

    def __init__(self, id, nodes):
        self.id = id
        self.nodes = nodes
    
    def __repr__(self):
        return f"Community({self.id}, nodes={self.nodes})"

def parse_file_day25(file_path, example: str = "") -> Any:
    if example:
        lines = [example]
    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
    wires = defaultdict(lambda: set())
    edges = set()
    vertices = set()
    for line in lines:
        curr = line.strip()

        origin, children = curr.split(": ")
        vertices.add(origin)
        for child in children.split():
            wires[origin].add(child)
            wires[child].add(origin)
            edges.add((origin, child))
            vertices.add(child)
    return Setting25(wires, edges, vertices)

def solve_day25_part1(input: Setting25) -> int: 
    # https://en.wikipedia.org/wiki/Karger%27s_algorithm
    # Karger's impl from: https://gist.github.com/pmetzger/52781cb9ce98a1e13ac2d3dc6ae93292
    # I was accounting for the groups badly. I wanted to keep a set of the groups when it sufficed to keep the
    # a count of the size
    while True:
        # clone vertices and edges
        nodes = defaultdict(lambda: list())
        edges = [list(e) for e in input.edges]
        node_size = {v: 1 for v in input.vertices}
        random.shuffle(edges)
        
        for edge in edges:
            nodes[edge[0]].append(edge)
            nodes[edge[1]].append(edge)
        while len(nodes) > 2:
            e = edges.pop()
            u, v = e
            if u == v: 
                continue
            
            for edge in nodes[v]:
                for i in range(2):
                    if edge[i] == v:
                        edge[i] = u
                nodes[u].append(edge)
            del nodes[v]

            node_size[u] += node_size[v]
            del node_size[v]

            new_edges = []
            for edge in nodes[u]:
                up, vp = edge
                if up != vp:
                    new_edges.append(edge)
            nodes[u] = new_edges
        node_keys = list(nodes.keys())
        if len(nodes[node_keys[0]]) <= 3:
            break
    return node_size[node_keys[0]] * node_size[node_keys[1]]

    #     mult = 1
    #     for v in vertex:
    #         mult *= len(vertex_groups[v])

    #         freq[mult] += 1
        
    # for k in freq:
    #     print(k, freq[k])
    
    # # networkx solution
    # G = nx.Graph()
    # for e in input.edges:
    #     G.add_edge(*e)
    # cc = nx.spectral_bisection(G)
    # return len(cc[0]) * len(cc[1])

def solve_day25_part2(input: Setting25) -> int:
    return 0

def solve_day25(input: Setting25, expected_pt1: Optional[int] = None, expected_pt2: Optional[int] = None):
    out_part1 = solve_day25_part1(input)

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

    out_part2 = solve_day25_part2(input)
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

def main_25(run_all: bool = False, example: Optional[str] = None, answer_only: bool = False):
    if not answer_only:
        if example:
            print("Testing input from cmd line")
            input = parse_file_day25("", example=example)
            solve_day25(input)
            exit(0)

        print("Running script for day 25")
        print("Sample input")
        print("---------------------------------")
        expected_out_part1 = 54
        expected_out_part2 = None
        print("Input file:", sample_file_path)
        input = parse_file_day25(sample_file_path)
        solve_day25(input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2)

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day25(input_file_path)
        solve_day25(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--actual', action='store_true')
    parser.add_argument('-e', '--example')
    parser.add_argument('-o', '--answer-only', action='store_true')
    args = parser.parse_args()
    main_25(run_all=args.actual, example=args.example, answer_only=args.answer_only)
