import numpy as np

from transporter.data.create_data.Graph import Graph
from transporter.measurement.DrawingFunctionPerformance import DrawingFunctionPerformance
from transporter.data.create_data.FileManager import FileManager
from transporter.transporter.GA_refactoring.GA_refactoring import HGA, get_dir_path
from transporter.transporter.GA_legacy.GA_legacy import run_ga

import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 폰트 세팅 맥
# font_path = r'C:\Windows\Fonts\gulim.ttc'
# font = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font)
font_path = r'C:\Windows\Fonts\gulim.ttc'

font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
plt.rcParams['axes.unicode_minus'] = False

cluster = 2
block = 300

ga_params = {
    'POPULATION_SIZE': 100,
    'GENERATION_SIZE': 300,
    'ELITISM_RATE': 0.05,
    'MUTATION_RATE': 0.01,
    'SELECTION_METHOD': 'selection2',
}
precondition = {
    'START_TIME': 9,  # 전제
    'FINISH_TIME': 18,  # 전제
    'LOAD_REST_TIME': 0.3,  # 전제
    'BLOCKS': block,  # 전제
}

data_path = os.path.join(get_dir_path("transporter"), "data")
node_file_path = os.path.join(data_path, "nodes_and_blocks", "cluster", "simply_mapping", str(cluster), f"node.csv")
block_path = os.path.join(data_path, "nodes_and_blocks", "cluster", "simply_mapping", str(cluster), f"block{block}.csv")

transporter_path = os.path.join(data_path, 'transporters', 'transporter.csv')

file_manager = FileManager()
graph = Graph(node_file_path)
transporter_container = file_manager.load_transporters(transporter_path)


'''
    진화가 진행되면서 우수한 개체를 뽑기 때문에 중복되는 개체가 생기게 되는데
    중복되는 개체에 대해서 시각적인 그래프로 출력하는 파일
'''

def plot_graphs(x, y_list, labels, title):
    for y, label in zip(y_list, labels):
        plt.plot(x[:len(y)], y, label=label)

    plt.title(title)
    plt.legend()
    plt.show()

def plot_fitness(results, labels): # result col: 세대 row: 세대별 적합도
    plt.figure(figsize=(15, 5), dpi=300)
    fig, ax = plt.subplots()


    for idx, fitness in enumerate(results):
        max_fitnesses = []  # 각 세대에서 가장 높은 적합도를 저장할 리스트
        median_fitnesses = []  # 각 세대에서 중앙값을 저장할 리스트
        min_fitnesses = []  # 각 세대에서 가장 낮은 적합도를 저장할 리스트
        for generation in fitness:

            max_fitness = max(generation)  # 해당 세대에서 가장 높은 적합도
            min_fitness = min(generation)  # 해당 세대에서 가장 낮은 적합도
            median_fitness = np.average(generation)  # 해당 세대에서 중앙값

            max_fitnesses.append(max_fitness)
            median_fitnesses.append(median_fitness)
            min_fitnesses.append(min_fitness)
        # 그래프 그리기

        ax.fill_between(range(len(min_fitnesses)), min_fitnesses, max_fitnesses, alpha=0.4, linewidth=0)
        # 세대에서 가장 높은 적합도, 중앙값, 가장 낮은 적합도를 그래프에 추가
        plt.plot(median_fitnesses, label=labels[idx])
    plt.legend()
    plt.xlabel('세대')
    plt.ylabel('적합도')
    plt.title('세대별 개체별 적합도')
    # plt.savefig("30gen2selectionk10.png", dpi=300)

    plt.show()




def a(block_container, container_title):
    method_key = ['selection2']
    result_key = ['best_individual', 'work_tp_count', 'best_fitness']
    result_dict = dict()
    for i in range(len(method_key)):
        result_dict[method_key[i]] = HGA(transporter_container, block_container, graph, ga_params, precondition).run_GA()
    # 변환할 딕셔너리 초기화
    result = {key1: {key2: None for key2 in method_key} for key1 in result_key}
    # 변환 수행
    for key1, val1 in result_dict.items():
        for key2, val2 in val1.items():
            result[key2][key1] = val2

    for ret_key in result.keys():  # best, work, fitness
        values = []
        if ret_key == 'work_tp_count':
            for method in method_key:
                values.append(result[ret_key][method])
            plot_graphs(range(len(values[0])), values, method_key, container_title + " " + ret_key)

        if ret_key == 'best_fitness':
            for method in method_key:
                values.append(result[ret_key][method])

            plot_fitness(values, method_key)

    # time_set = {
    #     'start_time': config_dict['START_TIME'],
    #     'end_time': config_dict['FINISH_TIME'],
    #     'load_rest_time': config_dict['LOAD_REST_TIME'],
    # }
    # multi_start = MultiStart(transporter_container, random_block_container, graph, 50, time_set)
    # print("multistart")
    # multi_start.run()
    # for i in range(len(multi_start.fitness_values)):
    #     plt.plot(1, multi_start.fitness_values[i], marker='o', linestyle='', color='black')




if __name__ == '__main__':
    filemanager = FileManager()
    graph = Graph(node_file_path)
    transporter_container = filemanager.load_transporters(transporter_path)
    block_container = filemanager.load_block_data(block_path, BLOCK_NUM=precondition['BLOCKS'])
    ga = HGA(transporter_container, block_container, graph, ga_params, precondition).run_GA()
    data = ga['fitness']

    # 데이터의 행 수와 열 수
    num_rows = len(data)
    num_cols = len(data[0])

    # 그래프 그리기
    plt.figure(figsize=(10, 6))  # 그래프 크기 설정

    for i in range(num_rows):
        y_values = data[i]
        plt.scatter([i] * num_cols, y_values, s=10)  # 각 요소를 점으로 찍기

    plt.xlabel('Generation')  # x축 레이블
    plt.ylabel('Fitness')  # y축 레이블
    plt.title('세대별 적합도 수렴그래프')  # 그래프 제목


    plt.show()  # 그래프 보이기
    # for i in range(1):
    #     a(block_container, 'Random Blocks')
