import numpy as np

from transporter.data.create_data.Graph import Graph
from transporter.measurement.DrawingFunctionPerformance import DrawingFunctionPerformance
from transporter.data.create_data.FileManager import FileManager
from transporter.transporter.GA_refactoring.GA_refactoring import GA
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

transporter_path = os.path.join(os.getcwd(), '../transporter', 'create_data', 'nodes_and_blocks', 'transporter.csv')
random_block_path = os.path.join(os.getcwd(), '../transporter', 'create_data', 'nodes_and_blocks', 'Blocks.csv')
heavy_block_path = os.path.join(os.getcwd(), '../transporter', 'create_data', 'nodes_and_blocks', 'heavyBlocks.csv')
light_block_path = os.path.join(os.getcwd(), '../transporter', 'create_data', 'nodes_and_blocks', 'lightBlocks.csv')
node_file_path = os.path.join(os.getcwd(), '../transporter', "create_data", "nodes_and_blocks", "node.csv")

file_manager = FileManager()
graph = Graph(node_file_path)
transporter_container = file_manager.load_transporters(transporter_path)
light_block_container = file_manager.load_block_data(light_block_path)
heavy_block_container = file_manager.load_block_data(heavy_block_path)
random_block_container = file_manager.load_block_data(random_block_path)

config_dict = {
    'POPULATION_SIZE': 100, # 한 세대에서의 인구 수를 설정합니다.
    'GENERATION_SIZE': 1000,  # 몇 세대에 걸쳐 진화할 지 설정합니다.
    'LOAD_REST_TIME': 0.3,  # 트랜스포터가 목적지에서 물건을 실어나르는 시간을 설정합니다 (시)
    'ELITISM_RATE': 0.02,  # 엘리트 individual의 비율을 결정합니다.
    'MUTATION_RATE': 0.05,  # 돌연변이가 일어날 확률을 설정합니다.
    'START_TIME': 9,  # 일과의 시작시간을 결정합니다.
    'FINISH_TIME': 18,  # 일과가 끝나는 시간을 결정합니다.
    'BLOCKS': 100,  # 총 블록 수를 설정합니다. 최대 100개까지 설정가능합니다.
}

'''
    진화가 진행되면서 우수한 개체를 뽑기 때문에 중복되는 개체가 생기게 되는데
    중복되는 개체에 대해서 시각적인 그래프로 출력하는 파일
'''
def compareToLegacy():
    ga = GA(transporter_container, random_block_container, config_dict)

    dfp = DrawingFunctionPerformance(
        ga.run_GA,
        run_ga,
        (),
        (transporter_container, random_block_container),
        5
    )

    dfp.draw_performance_graph()
    dfp.draw_time_graph()
    dfp.show()


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
    plt.savefig("30gen2selectionk10.png", dpi=300)

    plt.show()




def a(block_container, container_title):
    method_key = ['selection2']
    result_key = ['best_individual', 'work_tp_count', 'fitness']
    result_dict = dict()
    for i in range(len(method_key)):
        result_dict[method_key[i]] = GA(transporter_container,
                                         block_container, graph, config_dict, selection_method=method_key[i]).run_GA()
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

        if ret_key == 'fitness':
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
    for i in range(1):
        a(random_block_container, 'Random Blocks')
