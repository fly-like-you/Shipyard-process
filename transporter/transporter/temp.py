import os
import networkx as nx
import pandas as pd
import math
import matplotlib.pyplot as plt
map_path = os.path.join(os.getcwd(), 'create_data', 'data', 'map.xlsx')

# xlsx 파일에서 좌표 데이터를 읽어옴
df = pd.read_excel(map_path)

# 빈 그래프 생성
G = nx.Graph()

# 노드 추가
for i in range(len(df)):
    G.add_node(df.loc[i, 'no'])

# 이웃한 노드에 대해서만 간선 추가
for i in range(len(df) - 1):
    if df.loc[i+1, 'no'] - df.loc[i, 'no'] == 1:
        x1, y1 = df.loc[i, 'x'], df.loc[i, 'y']
        x2, y2 = df.loc[i+1, 'x'], df.loc[i+1, 'y']
        distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        weight = int(distance)
        G.add_edge(df.loc[i, 'no'], df.loc[i+1, 'no'], weight=weight)

# 노드의 위치를 지정한 딕셔너리 생성
pos = {df.loc[i, 'no']: (df.loc[i, 'x'], df.loc[i, 'y']) for i in range(len(df))}

# 그래프 시각화
nx.draw(G, pos=pos, with_labels=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show()
paths = nx.single_source_shortest_path(G, source=0)
print(paths)