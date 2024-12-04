# Stoer–Wagner
vertex = {v for v in input.vertices}
edges = {e for e in input.edges}

for i in range(1):
    init = random.choice([*vertex])
    A = set([init])
    add_order = [init]
    while len(A) != len(vertex):
        best_num = 0
        best_vert = ""
        best = ""
        for v in A:
            for child in input.wires[v]:
                count = 0
                if child in A:
                    continue
                for o in input.wires[child]:
                    if o in A:
                        count += 1
                if count > best_num:
                    best_num = count
                    best = child
        A.add(best)
        add_order.append(best)
    print(best, add_order)
