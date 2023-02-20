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


    def create_block_from_map_file(self, file_path, BLOCK_NUM):

        file = pathlib.Path(file_path)

        if file.exists():
            df = pd.read_excel(file, engine='openpyxl')
            for i in range(1, BLOCK_NUM + 1):
                w = random.random()
                if w <= 0.07:
                    w = random.randint(1, 50)
                elif w <= 0.18:
                    w = random.randint(50, 150)
                elif w <= 0.29:
                    w = random.randint(150, 250)
                elif w <= 0.47:
                    w = random.randint(250, 350)
                elif w <= 0.66:
                    w = random.randint(350, 450)
                elif w <= 0.81:
                    w = random.randint(450, 500)
                elif w <= 0.92:
                    w = random.randint(500, 600)
                elif w <= 1:
                    w = random.randint(600, 700)

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
    blocks = FileManager()
    map_path = os.path.join(os.getcwd(), 'data', 'map.xlsx')
    block_path = os.path.join(os.getcwd(), 'data', 'blocks.csv')
    block_container = blocks.load_block_data(block_path)
