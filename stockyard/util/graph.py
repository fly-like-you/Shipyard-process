import networkx as nx
from networkx.algorithms import bipartite
from copy import deepcopy
from random import randint, shuffle


def graph(bipartite0, bipartite1, edge):
    B = nx.Graph()
    # Add nodes with the node attribute "bipartite"
    B.add_nodes_from(bipartite0, bipartite=0)
    B.add_nodes_from(bipartite1, bipartite=1)
    # Add edges only between nodes of opposite node sets
    B.add_edges_from(edge)

    hopcroft_karp_matching = bipartite.matching.hopcroft_karp_matching(B, bipartite0)
    print(hopcroft_karp_matching)
    eppstein_matching = bipartite.matching.hopcroft_karp_matching(B, bipartite0)
    print(eppstein_matching)

    print(nx.is_connected(B))
    # bottom_nodes, top_nodes = bipartite.sets(B)
    top_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}
    bottom_nodes = set(B) - top_nodes
    print(bottom_nodes)
    print(top_nodes)
    print(round(bipartite.density(B, bottom_nodes), 2))
    # G = bipartite.projected_graph(B, top_nodes)


if __name__ == '__main__':
    node_num = 50
    access_length = 5

    bipartiteA = [i for i in range(node_num)]
    bipartiteB = [str(i) for i in bipartiteA]
    # bipartiteB = deepcopy(str(bipartiteA))
    print(bipartiteB)
    edge = []
    for i in bipartiteA:
        left = i - randint(0, access_length)
        right = i + randint(1, access_length)
        # left = i - access_length
        # right = i + access_length
        if left < 0:
            left = 0
        if right > len(bipartiteA):
            right = len(bipartiteA)

        temp = []
        for j in range(left, right):
            # if not i == j:
            #     temp.append(str(j))
            temp.append(str(j))
        edge.append(temp)
    print(edge)
    edge_list = []

    for i in bipartiteA:
        for j in edge[i]:
            edge_list.append([i, j])

    # shuffle(bipartiteA)
    # bipartiteB = [str(i) for i in bipartiteA]
    # print(bipartiteB)

    graph(bipartiteA, bipartiteB, edge_list)

