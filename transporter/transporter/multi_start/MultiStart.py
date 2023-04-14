import pandas as pd

from transporter.transporter.GA_refactoring.Population import Population
from transporter.data.create_data.FileManager import FileManager
from transporter.data.create_data.Graph import Graph
from transporter.transporter.GA_refactoring.Fitness import Fitness
import os

def get_dir_path(target):
    file_path = os.getcwd()
    target_dir = target

    # 경로를 분할합니다.
    path_parts = os.path.normpath(file_path).split(os.sep)

    # 특정 디렉터리까지의 인덱스를 찾습니다.
    index = path_parts.index(target_dir)

    # 해당 인덱스까지의 경로를 조합합니다.
    target_path_parts = path_parts[:index + 1]

    # 드라이브 문자와 경로를 올바르게 결합합니다.
    if os.name == 'nt' and len(target_path_parts[0]) == 2:  # 윈도우 드라이브 문자 (예: C:)
        target_path = os.path.join(target_path_parts[0] + os.sep, *target_path_parts[1:])
    else:
        target_path = os.path.join(*target_path_parts)

    return target_path

cluster = "cluster4"
data_path = os.path.join(get_dir_path("transporter"), "data")
node_file_path = os.path.join(data_path, "nodes_and_blocks", "cluster", "simply_mapping", f"node({cluster}).csv")
transporter_path = os.path.join(data_path, 'transporters', 'transporter.csv')
block_path = os.path.join(data_path, "nodes_and_blocks", "cluster", "simply_mapping", f"block({cluster}).csv")


class MultiStart:
    def __init__(self, transporter_container, block_container, graph, size, time_set):
        self.transporter_container = transporter_container
        self.block_container = block_container
        self.graph = graph
        self.size = size
        self.shortest_path_dict = graph.get_shortest_path_dict()
        self.time_set = time_set
        self.fitness_values = None


    def run(self):

        population = Population(self.transporter_container, self.block_container, self.size)
        population.generate_population()
        population = population.get_population()

        self.fitness_values = Fitness.get_fitness_list(population, self.shortest_path_dict, self.time_set)





if __name__ == "__main__":
    ga_params = {
        'POPULATION_SIZE': 100,
        'GENERATION_SIZE': 500,
        'ELITISM_RATE': 0.05,
        'MUTATION_RATE': 1,
        'SELECTION_METHOD': 'selection2',
    }
    precondition = {
        'START_TIME': 9,  # 전제
        'FINISH_TIME': 18,  # 전제
        'LOAD_REST_TIME': 0.3,  # 전제
        'BLOCKS': 100,  # 전제
    }


    filemanager = FileManager()

    graph = Graph(node_file_path)
    transporter_container = filemanager.load_transporters(transporter_path)
    block_container = filemanager.load_block_data(block_path, 100)
    time_set = {
        'start_time': precondition['START_TIME'],
        'end_time': precondition['FINISH_TIME'],
        'load_rest_time': precondition['LOAD_REST_TIME'],
    }
    result = []

    for i in range(300):
        print(i)
        multi_start = MultiStart(transporter_container, block_container, graph, 100, time_set)
        multi_start.run()
        a = sorted(multi_start.fitness_values, reverse=True)[0]
        result.append({
            'fitness': a,
        })
    df_results = pd.DataFrame(result).sort_values(by='fitness', ascending=False)
    df_results.to_pickle(f'cluster/{cluster}_multi_start(len300).pkl')

    print(result)



