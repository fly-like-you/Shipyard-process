import networkx as nx

G = nx.Graph()
G.add_edge(1, 2, weight=4)
G.add_edge(2, 3, weight=2)
G.add_edge(3, 4, weight=3)
G.add_edge(4, 4, weight=4)
G.add_edge(4, 5, weight=5)

# 여러 노드 쌍 간의 거리 계산
distances = nx.shortest_path_length(G, weight='weight')
print(dict(distances))