import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math


class Graph:
    def __init__(self, csv_file_path):
        self.graph = nx.Graph()
        self.from_csv(csv_file_path)

    def from_csv(self, csv_file_path):
        df = pd.read_csv(csv_file_path)
        for i in range(len(df)):

            self.add_node(df.loc[i, "no"], df.loc[i, "x"], df.loc[i, "y"])
        for i in range(len(df)):
            edges = str(df.loc[i, "edge"]).split(" ")
            for edge in edges:
                if edge:
                    self.add_edge(df.loc[i, "no"], int(edge))

    def add_node(self, node_id, x, y):
        self.graph.add_node(node_id, pos=(x, y))

    def add_edge(self, node_id1, node_id2):
        pos = nx.get_node_attributes(self.graph, "pos")
        distance = int(math.dist(pos[node_id1], pos[node_id2])) * 2
        self.graph.add_edge(node_id1, node_id2, weight=distance)

    def node_distance(self, node1, node2):
        return nx.shortest_path_length(self.graph, source=node1, target=node2, weight='weight')

    def get_shortest_path_dict(self):
        return dict(nx.shortest_path_length(self.graph, weight='weight'))

    def get_node_attr(self):
        return nx.get_node_attributes(self.graph, "pos")

    def draw(self):
        pos = nx.get_node_attributes(self.graph, "pos")
        labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw(self.graph, pos=pos, with_labels=True, node_size=50, font_size=5)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, font_size=5)
        plt.show()



# node_file_path = os.path.join(os.getcwd(), "data", "node(cluster3).csv")
# g = Graph()
# g.from_csv(node_file_path)
# g.draw()
#
# distance = nx.shortest_path_length(g.graph, source=1, target=24, weight='weight')
# print(distance)