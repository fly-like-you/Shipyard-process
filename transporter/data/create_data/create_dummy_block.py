import csv
from transporter.data.create_data.Block import Block
import pandas as pd
import random


class BlockGenerator:
    def __init__(self, node_path, block_num, weight_style='heavy'):
        self.node_path = node_path
        self.block_num = block_num
        self.weight_style = weight_style
        self.blocks = []
        self.clusters = self.__create_clusters()

    def create_block_from_graph_file(self):
        print("모든 클러스터 내의 노드 수가 같아야 합니다.")
        for i in range(1, self.block_num + 1):
            w = self.__set_block_weight()
            start_node, end_node = self.__set_block_start_end_node()
            start_time, end_time = self.__set_block_start_end_time()

            self.blocks.append(Block(i, w, start_node, end_node, start_time, end_time))

    def write_csv(self, file_path):
        with open(file_path, mode='w', newline='') as csv_file:
            fieldnames = ['no', 'weight', 'start_node', 'end_node', 'start_time', 'end_time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()

            for block in self.blocks:
                writer.writerow({
                    'no': block.no,
                    'weight': block.weight,
                    'start_node': block.start_node,
                    'end_node': block.end_node,
                    'start_time': block.start_time,
                    'end_time': block.end_time
                })

    def __set_block_weight(self):
        weight_list = [0.01, 0.06, 0.10, 0.18, 0.19, 0.20, 0.21, 0.06]

        if self.weight_style == 'light':
            weight_list.reverse()
        elif self.weight_style == 'random':
            weight_list = [1 for _ in range(1, 9)]

        weight_prob = random.choices(range(1, 9), weights=weight_list)
        w = random.randint(weight_prob[0] * 100 - 100, weight_prob[0] * 100)
        while w < 50:
            w = random.randint(weight_prob[0] * 100 - 100, weight_prob[0] * 100)

        return w

    def __create_clusters(self):
        df = pd.read_csv(self.node_path)
        cluster_size = 9
        node_count = len(df)
        clusters = []
        if node_count % cluster_size != 0:
            raise ValueError("노드 개수와 클러스터 크기가 나누어 떨어져야 합니다.")

        for i in range(node_count // cluster_size):
            start_node = i * cluster_size + 1
            end_node = start_node + cluster_size - 1
            clusters.append((start_node, end_node))

        return clusters

    def __set_block_start_end_node(self, inner_cluster_prob=0.7):
        if random.random() < inner_cluster_prob:
            # 클러스터 내에서 뽑음
            cluster_index = random.randint(0, len(self.clusters) - 1)
            cluster = range(self.clusters[cluster_index][0], self.clusters[cluster_index][1])
            start_node, end_node = random.sample(cluster, k=2)
        else:
            # 클러스터 사이에서 뽑음
            start_cluster_index, end_cluster_index = random.sample(range(0, len(self.clusters)), k=2)
            start_node = random.randint(self.clusters[start_cluster_index][0], self.clusters[start_cluster_index][1])
            end_node = random.randint(self.clusters[end_cluster_index][0], self.clusters[end_cluster_index][1])

        return start_node, end_node

    def __set_block_start_end_time(self):
        start_time = 9
        if random.random() <= 0.7:
            start_time = random.randint(9, 13)

        end_time = random.randint(9, 18)
        while start_time + 4 > end_time:
            end_time = random.randint(9, 18)

        return start_time, end_time



if __name__ == '__main__':
    import os
    node_file_path = os.path.join(os.getcwd(), '../../transporter', "create_data", "../nodes_and_blocks", "cluster", "node(cluster4).csv")
    bg = BlockGenerator(node_file_path, 100, weight_style='random')
    bg.create_block_from_graph_file()
