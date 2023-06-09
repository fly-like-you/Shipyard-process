from transporter.transporter.none_hybrid.NoneHybrid import GA
from transporter.transporter.GA_refactoring.GA_refactoring import HGA
from transporter.transporter.multi_start.MultiStart import MultiStart, get_dir_path
from transporter.data.create_data.FileManager import FileManager
from transporter.data.create_data.Graph import Graph
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt

import pickle
import os

font_path = r'C:\Windows\Fonts\gulim.ttc'
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
plt.rcParams['axes.unicode_minus'] = False

block = 100
cluster = 2

ga_params = {
    'POPULATION_SIZE': 100,
    'GENERATION_SIZE': 400,
    'ELITISM_RATE': 0.05,
    'MUTATION_RATE': 0.1,
    'SELECTION_METHOD': 'selection2',
}


precondition = {
    'START_TIME': 9,  # 전제
    'FINISH_TIME': 18,  # 전제
    'LOAD_REST_TIME': 0.2,  # 전제
    'BLOCKS': block,  # 전제
}

data_path = os.path.join(get_dir_path("transporter"), "data")
filemanager = FileManager()

# 그래프 파일 받아오기
node_file_path = os.path.join(data_path, "nodes_and_blocks", "cluster", "simply_mapping", str(cluster), f"node.csv")
graph = Graph(node_file_path)
shortest_path_dict = graph.get_shortest_path_dict()

# 블록 받아오기
block_path = os.path.join(data_path, "nodes_and_blocks", "cluster", "simply_mapping", str(cluster), f"block{block}.csv")
block_container = filemanager.load_block_data(block_path, BLOCK_NUM=precondition['BLOCKS'])

# 트랜스포터 받아오기
transporter_path = os.path.join(data_path, 'transporters', 'transporter.csv')
transporter_container = filemanager.load_transporters(transporter_path)
hga = HGA(transporter_container, block_container, graph, ga_params, precondition)
ga = GA(transporter_container, block_container, graph, ga_params, precondition)
ms = MultiStart(transporter_container, block_container, graph, ga_params, precondition)

result_dict = {'HGA': [], "GA": [], "MS": []}
for i in range(5):
    result_dict['MS'].append(ms.run_GA())
    result_dict['GA'].append(ga.run_GA())
    result_dict['HGA'].append(hga.run_GA())

with open('./compare_3algorithm.pickle', 'rb') as f:
    result_dict = pickle.load(f)