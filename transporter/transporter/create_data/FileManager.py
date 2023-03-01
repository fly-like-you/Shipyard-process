import os
import pathlib
import random
import sys
import pandas as pd
from transporter.transporter.create_data.Transporter import Transporter
from transporter.transporter.create_data.Block import Block

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


    def create_block_from_map_file(self, file_path, BLOCK_NUM, weight_style='heavy'):
        weight_list = [0.01, 0.06, 0.10, 0.18, 0.19, 0.20, 0.21, 0.06]

        if weight_style == 'light':
            weight_list.reverse()
        elif weight_style == 'random':
            weight_list = [1 for _ in range(1, 9)]

        file = pathlib.Path(file_path)

        if file.exists():
            df = pd.read_excel(file, engine='openpyxl')
            for i in range(1, BLOCK_NUM + 1):
                weight_prob = random.choices(range(1, 9), weights=weight_list)
                w = random.randint(weight_prob[0] * 100 - 100, weight_prob[0] * 100)

                node1 = df.sample()
                node2 = df.sample()

                start_node = node1['no'].values[0]
                end_node = node2['no'].values[0]

                while start_node == end_node:  # 시작 노드, 종료 노드가 달라야 함
                    node1 = df.sample()
                    start_node = node1['no'].values[0]

                start_time = 9
                if random.random() <= 0.7:
                    start_time = random.randint(9, 13)

                end_time = random.randint(9, 18)
                while start_time + 4 > end_time:  # 최소 작업시간이 4시간 이상 이어야 함
                    end_time = random.randint(9, 18)

                start_pos = [node1['x'].values[0], node1['y'].values[0]]
                end_pos = [node2['x'].values[0], node2['y'].values[0]]

                self.blocks.append(Block(i, w, start_node, end_node, start_time, end_time, start_pos, end_pos))
            return self.blocks
        else:
            print(-1)

    def load_block_data(self, file_path, BLOCK_NUM=100):
        block_df = pd.read_csv(file_path)

        for i in range(BLOCK_NUM):
            block_list = []
            df = pd.read_csv(file_path)
            for i, (no, weight, start_node, end_node, start_time, end_time, start_pos, end_pos) in enumerate(
                    zip(df['no'], df['weight'], df['start_node'], df['end_node'], df['start_time'], df['end_time'],
                        df['start_pos'], df['end_pos'])):
                if i >= BLOCK_NUM:
                    break
                start_pos = [int(x) for x in start_pos.strip('[]').split(',')]
                end_pos = [int(x) for x in end_pos.strip('[]').split(',')]
                block = Block(no, weight, start_node, end_node, start_time, end_time, start_pos, end_pos)
                block_list.append(block)
            return block_list




if __name__ == '__main__':
    file_manager = FileManager()
    map_path = os.path.join(os.getcwd(), 'data', 'map.xlsx')
    block_path = os.path.join(os.getcwd(), 'data', 'blocks.csv')
    block_container = file_manager.load_block_data(block_path)
    block_weight_list = []

    for block in block_container:
        block_weight_list.append(block.weight)
    from transporter.transporter.measurement.measureData import plot_histogram
    plot_histogram(block_weight_list, 700)



