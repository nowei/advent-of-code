from collections import defaultdict
import random
freq = defaultdict(lambda: 0)

# https://en.wikipedia.org/wiki/Karger%27s_algorithm

n = len(input.vertices)
m = len(input.edges)

for _ in range(n *n * n *m):
    # clone vertices and edges
    vertex = {v for v in input.vertices}
    vertex_groups = {v:set([v]) for v in input.vertices}
    edges = {e for e in input.edges}

    while len(vertex) > 2:
        e = random.choice([*edges])
        u, v = e
        edges.remove(e)
        # u_group = get_origin(u, vertex_groups)
        # v_group = get_origin(v, vertex_groups)
        u_group = vertex_groups[u]
        v_group = vertex_groups[v]
        if u_group == v_group: 
            continue
        else:
            new_group = u_group | v_group
            for s in new_group:
                vertex_groups[s] = new_group
                if s in vertex:
                    vertex.remove(s)
            min_node = ""
            if u < v:
                min_node = u
            else: # v < u
                min_node = v
            vertex.add(min_node)
            to_remove = set()
            to_add = set()
            for up, vp in edges:
                if vertex_groups[up] == new_group:
                    to_remove.add((up, vp))
                    to_add.add((min_node, vp))
                elif vertex_groups[vp] == new_group:
                    to_remove.add((up, vp))
                    to_add.add((up, min_node))
            edges = edges.difference(to_remove) | to_add
    mult = 1
    for v in vertex:
        mult *= len(vertex_groups[v])

        freq[mult] += 1
    
for k in freq:
    print(k, freq[k])