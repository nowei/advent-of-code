from typing import Dict, List, Tuple
from collections import deque
from rich import print as pprint

InputType = List[Tuple[str, List[str]]]
parent_path = "src/days/day11/"


def _parse_input(sample: bool, part: int) -> InputType:
    file_name = parent_path + "input.txt"
    if sample:
        file_name = parent_path + "sample.txt"
        if part == 2:
            file_name = parent_path + "sample-2.txt"

    lines = []
    with open(file_name, "r") as f:
        for line in f:
            source, destinations_str = line.strip().split(": ")
            destinations = tuple(destinations_str.split())
            lines.append((source, destinations))

    return lines


def part1(_input: InputType) -> int:
    # Generate a dag
    mapping = {}
    for source, destinations in _input:
        mapping[source] = destinations

    layers = deque(["you"])
    seen_outs = 0
    while layers:
        curr = layers.popleft()
        if curr == "out":
            seen_outs += 1
        if curr in mapping:
            next_section = mapping[curr]
            layers.extend(next_section)

    return seen_outs


def part2(_input: InputType) -> int:
    # Generate a dag
    mapping = {}
    for source, destinations in _input:
        mapping[source] = destinations
    all_paths: List[List[str]] = []
    curr_path = ["svr"]
    all_nodes = set()
    for source, dest in mapping.items():
        all_nodes.add(source)
        all_nodes.update(dest)
    print(len(all_nodes))
    # path contraction
    contracting = True
    curr_mapping = mapping
    keep_set = set(["out", "fft", "dac"])
    while contracting:
        path = ["svr"]
        seen = set()
        # At every jump,
        # we evaluate the next jump

        # def contracting_dfs(path):
        #     dests = curr_mapping[path[-1]]
        #     contracting = False
        #     next_level: list[str] = []
        #     for next_dest in dests:
        #         if next_dest not in keep_set:
        #             if len(curr_mapping[next_dest]) == 1:
        #                 next_level.append(curr_mapping[next_dest][0])
        #                 contracting = True
        #             else:
        #                 next_level.append(next_dest)
        #         else:
        #             next_level.append(next_dest)
        #     new_mapping[path[-1]] = next_level
        #     for d in next_level:
        #         if d != "out":
        #             contracting_dfs(path + [d])
        #     return contracting
        # contracting = contracting_dfs(path)
        contracting = False

        # TODO: New idea instead of fiddling around with jumps and skips and stuff...
        # Path compression using topological sort???
        def topo_sort_compression(mapping, all_nodes):
            # Basically the idea is to take a node, then keep going forward until we see a "dac" or "fft"
            # or we see a point where we need to wait until all other parts have come to the section...
            # At that point, we can compress the path from the start of the path going to the end. If it has
            # a dac or fft in the middle, then we keep it. Otherwise it is freely compressible.
            pass

        # Path compression using BFS
        # if A -> B -> C -> D, then A -> D
        # if A -> fft -> C -> D then A -> fft -> D
        # if A -> B -> fft -> D then A -> fft -> D
        # The same applies for DAC
        # if svr -> abc -> ccc
        #     \ ->  fft  --/
        # Then svr   ->   ccc
        #       \-> fft --/
        def bfs_layering(mapping, all_nodes):
            layers = [{"svr"}]
            node_origins: Dict[str, List] = {"svr": [1, []]}
            total_seen = 1
            seen: set[str] = set()
            while len(seen) != len(all_nodes):
                next_layer = set()
                for prev_node in layers[-1]:
                    seen.add(prev_node)
                    if prev_node not in mapping:  # out
                        continue
                    cand_nodes = mapping[prev_node]
                    for cand_node in cand_nodes:
                        if cand_node not in node_origins:
                            node_origins[cand_node] = [0, []]
                            total_seen += 1
                            next_layer.add(cand_node)
                        node_origins[cand_node][0] += 1
                        node_origins[cand_node][1].append((prev_node, len(layers)))
                layers.append(next_layer)
            assert_set: set[str] = set()
            for layer in layers:
                assert not assert_set.intersection(layer)
                assert_set.update(layer)
            pprint(node_origins)
            print(len(assert_set))

            new_mapping: Dict[str, List] = {}
            touched = set()
            skipped_set = set()
            for node, values in node_origins.items():
                layer_number, origins = values
                print("-------------------------------")
                print(new_mapping, touched)
                print(node, values, mapping.get(node, []))

                #      |
                #      v
                # A -> B -> C
                for prev_node_orig in origins:
                    prev_node, layer = prev_node_orig
                    if node not in keep_set:
                        print("node is not in keep set")
                        if len(mapping[node]) == 1:
                            # if prev_node in touched and prev_node in new_mapping:
                            #     print(f"skipping because {prev_node} has been touched")
                            #     continue
                            if prev_node in touched and prev_node not in skipped_set:
                                if prev_node not in new_mapping:
                                    new_mapping[prev_node] = []
                                print(
                                    "previous node was touched, so current node must be skipped"
                                )
                                new_mapping[prev_node].extend(list(mapping[node]))
                                skipped_set.add(node)
                            else:
                                print(
                                    "previous node was not touched, so it must be included"
                                )
                                new_mapping[node] = list(mapping[node])
                            touched.update(mapping[node])
                    else:  # Keep it
                        print("Evaluated node is in keep set, so it must be added")
                        if prev_node == "svr":
                            new_mapping[prev_node] = [node]
                        if node not in new_mapping:
                            new_mapping[node] = []
                        if node in ["out", "svr"]:
                            print("skipping because node is the start or end")
                            continue

                        new_mapping[node].extend(mapping[node])
                touched.add(node)
                print(new_mapping, touched)
            print("====================================")
            print("evaluation has ended...")
            all_new_nodes = set()
            for source, dest in new_mapping.items():
                all_new_nodes.add(source)
                all_new_nodes.update(dest)
            return new_mapping, all_new_nodes

        mapping_changed = True
        while mapping_changed:
            new_mapping, all_nodes = bfs_layering(mapping, all_nodes)
            print(new_mapping)
            print(all_nodes)
            mapping_changed = len(new_mapping) != len(mapping)
            mapping = new_mapping
        # def contract_mapping(mapping: dict) -> dict:
        #     new_mapping = {}
        #     contracted: dict = {}
        #     seen = set()
        #     for source, destinations in mapping.items():
        #         if len(destinations) == 1:
        #             dest = destinations[0]
        #             if dest in contracted:
        #                 new_mapping[source] = contracted[dest]
        #             if dest not in keep_set:
        #                 new_mapping[source] = mapping[dest]
        #                 contracted[dest] = mapping[dest]
        #             else:
        #                 new_mapping[source] = dest
        #     return new_mapping

        # new_mapping = contract_mapping(curr_mapping)
        # print(new_mapping)
        # contracting = len(new_mapping) != len(curr_mapping)
        # curr_mapping = new_mapping

    # can't easily work back from "out" because multiple
    # things

    # def dfs(path):
    #     dests = mapping[path[-1]]
    #     if "out" in dests:
    #         all_paths.append((path + ["out"]))
    #     else:
    #         for dest in dests:
    #             dfs(path + [dest])
    #     print(len(path), len(all_paths))

    # dfs(curr_path)
    # # bfs
    # layers: deque[Tuple[str, List[str]]] = deque([("svr", [])])
    # while layers:
    #     next_layer: deque[Tuple[str, List[str]]] = deque([])
    #     while layers:
    #         curr, path = layers.popleft()
    #         if curr in mapping:
    #             next_section = mapping[curr]
    #             for next in next_section:
    #                 next_layer.append((next, path + [curr]))
    #         elif curr == "out":
    #             all_paths.append((path + [curr]))
    #     layers = next_layer
    #     print(len(all_paths))
    print(len(all_paths))
    good_paths = 0
    for path in all_paths:
        if "fft" in path and "dac" in path:
            good_paths += 1
    return good_paths


def exec(part: int, execute: bool) -> int:
    _input = _parse_input(not execute, part)
    if part == 1:
        result = part1(_input)
    else:
        result = part2(_input)
    return result
