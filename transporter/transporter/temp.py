from transporter.transporter.GA_schedule.ScheduleGA import ScheduleGA
from transporter.transporter.create_data.Block import Block
from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.create_data.Graph import Graph
import matplotlib.pyplot as plt
import networkx as nx
import random
import imageio
import os

node_file_path = os.path.join(os.getcwd(), "create_data", "data", "node.csv")
transporter_path = os.path.join(os.getcwd(), 'create_data', 'data', 'transporter.csv')
block_path = os.path.join(os.getcwd(), 'create_data', 'data', 'Blocks.csv')

graph = Graph(node_file_path)
shortest_path_dict = graph.get_shortest_path_dict()
graph = graph.graph

file_manager = FileManager()
block_container = file_manager.load_block_data(block_path)

# 랜덤으로 블록 선택
blocks = []
tp_moving = []

for i in range(10):
    rand1, rand2 = random.sample(range(1, 39), k=2)

    block = Block(i + 1, 1, rand1, rand2, 1, 1)
    blocks.append(block)

ga = ScheduleGA(blocks, shortest_path_dict, population_size=100, max_generation=1500)
works = ga.run()
for i, block in enumerate(works):
    if i == 0:
        tp_moving.append([1, block.start_node])
        tp_moving.append([block.start_node, block.end_node])
    else:
        tp_moving.append([prev_block.end_node, block.start_node])
        tp_moving.append([block.start_node, block.end_node])
    prev_block = block

    print(f'Block {i} -> {block.start_node} to {block.end_node}')


# 기계 이동 궤적 그리기
pos = nx.get_node_attributes(graph, 'pos')
node_colors = []
node_size = []
for node in graph.nodes():
    node_colors.append("lightgray")
    node_size.append(100)

graph_edge_colors = ["lightgray" for _ in graph.edges()]

for i, move in enumerate(tp_moving, start=1):
    start_node = move[0]
    end_node = move[1]

    # 최단경로 계산
    shortest_path = nx.shortest_path(graph, start_node, end_node, weight="distance")
    print(shortest_path)
    # 노드 색상과 크기 변경
    node_colors[start_node - 1] = "red"
    node_colors[end_node - 1] = "green"
    node_size[start_node - 1] = 300
    node_size[end_node - 1] = 300

    # 간선 색상 변경
    edge_colors = ["black" if (u, v) in zip(shortest_path, shortest_path[1:]) or
                              (u, v) in zip(shortest_path[1:], shortest_path)
                   else "lightgray" for u, v in graph.edges()
                   ]
    for idx, color in enumerate(edge_colors):
        if color == 'black':
            graph_edge_colors[idx] = 'red'
    # 그래프 출력
    fig = plt.figure(figsize=(10, 7), dpi=150)
    nx.draw(graph, pos=pos, node_color=node_colors, node_size=node_size, edge_color=graph_edge_colors, width=2,
            with_labels=True)
    plt.annotate(f'Transporter: {tp_moving[i-1][0]} -> {tp_moving[i-1][1]}', xy=pos[start_node], fontsize=15)
    fig.savefig(f'./img/image_{i}.png')
    plt.show()

    for idx, color in enumerate(graph_edge_colors):
        if color == 'red':
            graph_edge_colors[idx] = 'black'

    node_colors[start_node - 1] = "gray"
    node_colors[end_node - 1] = "gray"

# 이미지를 이용해 GIF 생성
images = []
for i in range(1, len(tp_moving)):
    filename = f'./img/image_{i}.png'
    images.append(imageio.imread(filename))
imageio.mimsave('animation.gif', images, fps=0.5)





