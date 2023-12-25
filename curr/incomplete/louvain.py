ry combination of 3 wires.
    edges = input.edges
    C = {}
    id = 0
    communities = {}
    # Map vertices and edges into ids and create communities based on ids
    for v in input.vertices:
        C[v] = id
        communities[id] = Community(id, set([id]))
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
                k_i = k[id] # weighted_degree of i
                k_iin = 0 # the sum of the weights of the links between i and other nodes in the community that i is moving into
                for o_id in A[id]:
                    if o_id in neighbor.nodes:
                        k_iin += A[id][o_id]
                change = ((sum_in + 2 * k_iin) / (2 * m) - ((sum_tot + k_i)/(2 * m)) ** 2) - ((sum_in / (2 * m)) - (sum_tot / (2 * m)) ** 2 - (k_i / (2 * m)) ** 2)
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
            new_communities[id] = Community(id, set([id]))
            for c in community.nodes:
                old_community_to_new_community[c] = id
            id += 1
        for c_id in communities:
            community = communities[c_id]
            for id in community.nodes:
                new_id = old_community_to_new_community[id]
                for o_id in A[id]:
                    new_o_id = old_community_to_new_community[o_id]
                    new_A[new_id][new_o_id] += A[id][o_id]
        new_k = {}
        for id in new_communities:
            v = 0
            for o_id in new_A[id]:
                v += new_A[id][o_id]
            new_k[id] = v
        A = new_A
        k = new_k
        communities = new_communities
        print(A)
    mult = 1
    for c in communities:
        mult *= len(communities[c].nodes)
    return mult