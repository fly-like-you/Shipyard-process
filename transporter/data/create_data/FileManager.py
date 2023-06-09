import os
import pathlib
import sys
import pandas as pd

from transporter.data.create_data.Block import Block
from transporter.data.create_data.Transporter import Transporter


class FileManager:
    def __init__(self):
        self.osName = sys.platform
        self.blocks = []
        self.transporters = []
        self.nodes = []

    def load_transporters(self, file_path):
        file = pathlib.Path(file_path)

        if file.exists():
            df = pd.read_csv(file)
            temp = list(zip(df['no'] - 1, df['available_weight'], df['empty_speed'], df['work_speed']))
            for n, a, e, w in temp:
                self.transporters.append(Transporter(n, a, e, w))
            return self.transporters
        else:
            print(-1)
            return -1


    def load_block_data(self, file_path, BLOCK_NUM=100):
        df = pd.read_csv(file_path)

        block_list = []
        for i, (no, weight, start_node, end_node, start_time, end_time) in enumerate(
                zip(df['no'], df['weight'], df['start_node'], df['end_node'], df['start_time'], df['end_time'])):
            if i >= BLOCK_NUM:
                break

            # Block 생성 및 리스트에 추가
            block = Block(no, weight, start_node, end_node, start_time, end_time)
            block_list.append(block)
        return block_list

import matplotlib.pyplot as plt

def plot_weight_histogram(weight_list):
    bins = range(0, 900, 100)  # x축 구간 설정
    plt.hist(weight_list, bins=bins)
    plt.xticks(bins)
    plt.ylim(0, 30)

    plt.xlabel('Weight')
    plt.ylabel('Frequency')
    plt.title('Weight Histogram')
    plt.show()




if __name__ == '__main__':
    node_file_path = os.path.join(os.getcwd(), "../nodes_and_blocks", "node.csv")

    file_manager = FileManager()
    block_path = os.path.join(os.getcwd(), '../nodes_and_blocks', 'blocks.csv')
    block_li = file_manager.create_block_from_graph_file(node_file_path, 100, weight_style='heavy')
    weight_list = []
    for block in block_li:
        weight_list.append(block.weight)
        print(block.no, block.weight, block.start_node, block.end_node,
              block.start_time, block.end_time)


    plot_weight_histogram(weight_list)





