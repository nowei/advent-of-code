from typing import Any, Optional, Tuple, Dict, Set
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
    nodes: Set[int]
    all_nodes: Dict[int, str]

    def __init__(self, id, nodes, all):
        self.id = id
        self.nodes = nodes
        self.all = all

    def __repr__(self):
        return f"Community({self.id}, nodes={self.nodes}, all={self.all_nodes})"


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
    return solve_day25_part1_kargers_attmp2(input)


def solve_day25_part1_louvain_almost(input: Setting25) -> int:
    edges = input.edges
    C = {}
    id = 0
    communities = {}
    # Map vertices and edges into ids and create communities based on ids
    for v in input.vertices:
        C[v] = id
        communities[id] = Community(id, set([id]), {id: set([v])})
        id += 1
    A = defaultdict(lambda: dict())
    for u, v in edges:
        u_id = C[u]
        v_id = C[v]
        A[u_id][v_id] = 1
        A[v_id][u_id] = 1
    k = {}
    for id in communities:
        v = 0
        for o_id in A[id]:
            v += A[id][o_id]
        k[id] = v
    m = len(edges)
    node_to_community = {id: id for id in communities}
    # We thought about doing a min-cut/max-flow, but couldn't get it right.
    # We use a community-detection algorithm:
    while len(communities) > 2:
        print(len(communities))
        # Phase 1, move all nodes into a community with a modularity increase
        for id in communities:
            community = communities[id]
            community_id_to_consider = []
            for o_id in A[id]:
                if o_id not in community_id_to_consider:
                    community_id_to_consider.append(o_id)
            changes = []
            sum_in = 0
            sum_tot = 0
            for c_id in community.nodes:
                for o_id in A[c_id]:
                    if o_id in community.nodes:
                        sum_in += A[c_id][o_id]
                    sum_tot += A[c_id][o_id]
            for n_id in community_id_to_consider:
                neighbor = communities[n_id]
                k_i = k[id]  # weighted_degree of i
                k_iin = 0  # the sum of the weights of the links between i and other nodes in the community that i is moving into
                for o_id in A[id]:
                    if o_id in neighbor.nodes:
                        k_iin += A[id][o_id]
                change = (
                    (sum_in + 2 * k_iin) / (2 * m) - ((sum_tot + k_i) / (2 * m)) ** 2
                ) - (
                    (sum_in / (2 * m)) - (sum_tot / (2 * m)) ** 2 - (k_i / (2 * m)) ** 2
                )
                changes.append(change)
                # take_best positive change
            best = 0
            best_ind = -1
            for ind in range(len(changes)):
                if changes[ind] < 0:
                    continue
                if changes[ind] > best:
                    best_ind = ind
                    best = changes[ind]
            if best_ind >= 0:
                new_cid = community_id_to_consider[best_ind]
                old_cid = id
                communities[old_cid].nodes.remove(id)
                communities[new_cid].nodes.add(id)
                communities[new_cid].all[id] = communities[old_cid].all[id]
                # del communities[old_cid].all[id]
                node_to_community[old_cid] = new_cid
        to_remove = set()
        for c in communities.keys():
            if not communities[c].nodes:
                to_remove.add(c)
        for c in to_remove:
            communities.pop(c)

        # phase 2: group communities
        # all vertices in a community -> single vertex
        # all edges in a community -> self edges or outside edges
        new_communities = {}
        id = 0
        new_A = defaultdict(lambda: defaultdict(lambda: 0))
        old_community_to_new_community = {}
        for c_id in communities:
            community = communities[c_id]
            new_communities[id] = Community(id, set([id]), {id: set()})
            for c in community.nodes:
                old_community_to_new_community[c] = id
            id += 1
        for c_id in communities:
            community = communities[c_id]
            new_cid = old_community_to_new_community[c_id]
            for id in community.nodes:
                new_id = old_community_to_new_community[id]
                for o_id in A[id]:
                    new_o_id = old_community_to_new_community[o_id]
                    new_A[new_id][new_o_id] += A[id][o_id]
                new_communities[new_cid].all[new_cid] |= community.all[id]
        new_k = {}
        for id in new_communities:
            v = 0
            for o_id in new_A[id]:
                v += new_A[id][o_id]
            new_k[id] = v
        A = new_A
        k = new_k
        communities = new_communities
    mult = 1
    for c in communities:
        mult *= len(communities[c].all[c])
    return mult


def solve_day25_part1_kargers_attmp1(input: Setting25) -> int:
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


def solve_day25_part1_kargers_attmp2(input: Setting25) -> int:
    # https://en.wikipedia.org/wiki/Karger%27s_algorithm
    # Karger's impl from: https://gist.github.com/pmetzger/52781cb9ce98a1e13ac2d3dc6ae93292
    # I was accounting for the groups badly. I wanted to keep a set of the groups when it sufficed to keep the
    # a count of the size
    while True:
        # clone vertices and edges
        vertex = {v for v in input.vertices}
        vertex_groups = {v: set([v]) for v in input.vertices}
        edges = [list(e) for e in input.edges]
        nodes = {v: [] for v in input.vertices}

        for e in edges:
            nodes[e[0]].append(e)
            nodes[e[1]].append(e)

        random.shuffle(edges)

        while len(vertex) > 2:
            e = edges.pop()
            u, v = e
            u_group = vertex_groups[u]
            v_group = vertex_groups[v]
            if u_group == v_group:
                continue
            new_group = u_group | v_group
            for s in new_group:
                vertex_groups[s] = new_group
            for edge in nodes[v]:
                if edge[0] == v:
                    edge[0] = u
                if edge[1] == v:
                    edge[1] = u
                nodes[u].append(edge)
            vertex.remove(v)
            del nodes[v]
            new_edges = []
            for edge in nodes[u]:
                if edge[0] != edge[1]:
                    new_edges.append(edge)
            nodes[u] = new_edges
        mult = 1
        for v in vertex:
            mult *= len(vertex_groups[v])
        if all([len(nodes[v]) == 3 for v in vertex]):
            break

    return mult

    #     mult = 1
    #     for v in vertex:
    #         mult *= len(vertex_groups[v])

    #         freq[mult] += 1

    # for k in freq:
    #     print(k, freq[k])


def solve_day25_part1_nxg(input: Setting25) -> int:
    # networkx solution
    G = nx.Graph()
    for e in input.edges:
        G.add_edge(*e)
    cc = nx.spectral_bisection(G)
    return len(cc[0]) * len(cc[1])


def solve_day25_part2(input: Setting25) -> int:
    return 0


def solve_day25(
    input: Setting25,
    expected_pt1: Optional[int] = None,
    expected_pt2: Optional[int] = None,
):
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


def main_25(
    run_all: bool = False, example: Optional[str] = None, answer_only: bool = False
):
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
        solve_day25(
            input, expected_pt1=expected_out_part1, expected_pt2=expected_out_part2
        )

    if run_all:
        print("---------------------------------")
        print("Actual input")
        print("Input file:", input_file_path)
        input = parse_file_day25(input_file_path)
        solve_day25(input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--actual", action="store_true")
    parser.add_argument("-e", "--example")
    parser.add_argument("-o", "--answer-only", action="store_true")
    args = parser.parse_args()
    main_25(run_all=args.actual, example=args.example, answer_only=args.answer_only)
