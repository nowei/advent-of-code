from typing import List, Tuple, Dict, Union, Set
from collections import defaultdict

InputType = List[Tuple[str, str]]
parent_path = "src/days/day23/"


def _parse_input(sample: bool) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
    connections = []
    with open(file_name, "r") as f:
        for line in f:
            a, b = line.strip().split("-")
            connections.append((a, b))
    return connections


def create_graph(
    connections: List[Tuple[str, str]],
) -> Tuple[List[str], Dict[str, Set[str]]]:
    nodes = set()
    edges = defaultdict(set)
    for a, b in connections:
        nodes.add(a)
        nodes.add(b)
        edges[a].add(b)
        edges[b].add(a)
    return list(nodes), edges


def triplets(
    nodes: List[str], edges: Dict[str, Set[str]]
) -> List[Tuple[str, str, str]]:
    triplets = set()
    for a in nodes:
        a_edges = list(edges[a])
        for i in range(len(a_edges)):
            b = a_edges[i]
            for j in range(i + 1, len(a_edges)):
                c = a_edges[j]
                if b in edges[c]:
                    na, nb, nc = sorted([a, b, c])
                    triplets.add((na, nb, nc))
    return list(triplets)


def part1(_input: InputType) -> int:
    connections = _input
    nodes, edges = create_graph(connections)
    trips = triplets(nodes, edges)
    total = 0
    for cand in trips:
        a, b, c = cand
        if a.startswith("t") or b.startswith("t") or c.startswith("t"):
            total += 1
    return total


# bg,bu,ce,ga,hw,jw,nf,nt,ox,tj,uu,vk,wp
def _find_clique(cand: str, edges: Dict[str, Set[str]]) -> Set[str]:
    curr = set([cand])
    neighbors = set(edges[cand])
    # We don't need to revisit nodes we have already seen.
    visited = set()

    def _recurse(current_clique: Set[str], neighbors: Set[str]):
        best = current_clique
        for neighbor in neighbors:
            # To avoid revisiting cliques that we have seen, skip neighbors if they have
            # been seen during the recursion...
            if neighbor in best:
                continue
            if neighbor in visited:
                continue
            if all(c in edges[neighbor] for c in current_clique):
                nb_clone = set(neighbors)
                nb_clone.remove(neighbor)
                cand = _recurse(current_clique | set([neighbor]), nb_clone)
                if len(cand) > len(best):
                    best = cand
                # Note that we cannot unconditionally add the node to visited.
                # It may be the case that not all nodes are a part of a clique.
                # e.g. we have nodes A, B, C, and D.
                # if as a part of visiting the clique of size 2 (A, B) we saw C and D;
                # they would be added to the visited but not be part of the best set.
                # then the continue if neighbor in visited would skip over C and D
                # even if (A, C, D) was an even better clique...
                # Thus, we can only rule out the neighbor from consideration if it
                # was already part of a clique that is being evaluated, since the result
                # of each recursion will be the maximal clique possibly formed by the
                # current clique.
                visited.add(neighbor)
        return best

    return _recurse(curr, neighbors)


def find_largest_clique(nodes: List[str], edges: Dict[str, Set[str]]) -> List[str]:
    best_clique: List[str] = []
    # For each candidate, we only need to consider the set of edges
    # that were not found in the best clique for
    for cand, _cand_edges in sorted(edges.items(), key=lambda x: -len(x[1])):
        best_cand_clique = _find_clique(cand, edges)
        if len(best_cand_clique) > len(best_clique):
            best_clique = list(best_cand_clique)
    return best_clique


def part2(_input: InputType) -> str:
    connections = _input
    nodes, edges = create_graph(connections)
    best_clique = find_largest_clique(nodes, edges)
    return ",".join(sorted(best_clique))


def exec(part: int, execute: bool) -> Union[int, str]:
    _input = _parse_input(not execute)
    result: Union[int, str]
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
