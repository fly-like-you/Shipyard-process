import os
import random
import pandas as pd
import sys


class block:
    def __init__(self, no, weight, start_node, end_node, start_time, end_time, start_pos, end_pos):
        self.no = no  # 블록 번호
        self.weight = weight  # 블록 중량
        self.start_node = start_node  # 시작 노드
        self.end_node = end_node  # 종료 노드 (시작 노드에서, 종료 노드까지 운반)
        self.start_time = start_time  # 작업 운반 가능 시간
        self.end_time = end_time  # 작업 dead line
        self.start_pos = start_pos  # 시작 노드 좌표
        self.end_pos = end_pos  # 종료 노드 좌표

    def __str__(self):
        ret = 'no: {}, weight: {}, start_node: {}, end_node: {}, time: {} ~ {}, pos: {} -> {}'\
            .format(self.no, self.weight, self.start_node, self.end_node, self.start_time, self.end_time,
                    self.start_pos, self.end_pos)
        return ret

osName = sys.platform
if osName == 'win32':
    file_name = os.getcwd() + '\\create_data\\data\\map.xlsx'
elif osName == 'darwin':
    file_name = os.getcwd() + '/create_data/data/map.xlsx'

df = pd.read_excel(file_name, engine='openpyxl')
blocks = []
for i in range(1, 101):  # 옮겨야 할 블록 개수 (작업 개수)
    w = random.random()  # 가중치를 두고, 블록 생성
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

    start_node = random.randint(1, 30)
    end_node = random.randint(1, 30)
    while start_node == end_node:  # 시작 노드, 종료 노드가 달라야 함
        end_node = random.randint(1, 30)

    start_time = 9
    if random.random() <= 0.7:
        start_time = random.randint(9, 13)
    end_time = random.randint(9, 18)

    while start_time + 4 > end_time: # 최소 작업시간이 4시간 이상 이어야 함
        end_time = random.randint(9, 18)

    start_pos = [df.iloc[start_node]['x'], df.iloc[start_node]['y']]
    end_pos = [df.iloc[end_node]['x'], df.iloc[end_node]['y']]
    blocks.append(block(i, w, start_node, end_node, start_time, end_time, start_pos, end_pos))
