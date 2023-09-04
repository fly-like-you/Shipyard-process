import pickle

from matplotlib import pyplot as plt

from transporter.data.create_data.FileManager import FileManager
from transporter.transporter.GA_refactoring.Mutation import Mutation
from transporter.transporter.GA_refactoring.Selection import Selection
from transporter.transporter.GA_refactoring.Population import Population
from transporter.transporter.GA_refactoring.Fitness import Fitness
from transporter.transporter.GA_refactoring.Crossover import Crossover
from transporter.transporter.GA_schedule.ScheduleGA import ScheduleGA
from transporter.transporter.GA_refactoring.LocalSearch import LocalSearch
from transporter.data.create_data.Graph import Graph
from matplotlib import font_manager, rc

from tqdm import tqdm

import numpy as np
import copy

import os

font_path = r'C:\Windows\Fonts\gulim.ttc'

font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
plt.rcParams['axes.unicode_minus'] = False

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
        target_path = "/" + target_path

    return target_path


cluster = 2
block = 100

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


class SetSizeException(Exception):
    pass


def data_test(inspect_population, blocks):  # 블록 개수와 블록 중복 체크
    # given
    block_overlap_set = set()

    # when
    for transporter_list in inspect_population:
        for transporter in transporter_list:
            process = transporter.works

            for block in process:
                block_overlap_set.add(block.no)

    # then
    if len(block_overlap_set) != blocks:
        raise SetSizeException(f"Set size is not 30! generation")


class HGA:
    def __init__(self, transporter_container, block_container, graph, ga_params, precondition):
        self.transporter_container = transporter_container
        self.block_container = block_container
        self.graph = graph

        # 전제 조건
        self.time_set = {
            'start_time': precondition['START_TIME'],
            'end_time': precondition['FINISH_TIME'],
            'load_rest_time': precondition['LOAD_REST_TIME'],
        }
        self.BLOCKS = precondition['BLOCKS']

        # 알고리즘 파라미터
        self.POPULATION_SIZE = ga_params['POPULATION_SIZE']
        self.GENERATION_SIZE = ga_params['GENERATION_SIZE']
        self.ELITISM_RATE = ga_params['ELITISM_RATE']
        self.MUTATION_RATE = ga_params['MUTATION_RATE']
        self.selection_method = ga_params['SELECTION_METHOD']

        self.shortest_path_dict = graph.get_shortest_path_dict()
        self.population = Population(transporter_container, block_container, self.POPULATION_SIZE)
        self.population.generate_population()

    def get_best_solution(self, fitness_values, population):
        def get_transporter_count(individual):
            work_tp_count = 0
            for transporter in individual:
                if transporter.works:
                    work_tp_count += 1
            return work_tp_count

        best_idx = np.argmax(fitness_values)
        best_fitness = fitness_values[best_idx]
        best_individual = population[best_idx]
        best_transporter_count = get_transporter_count(best_individual)

        return best_fitness, best_transporter_count, best_individual


    def run_GA(self):
        population = self.population.get_population()
        mutation = Mutation(self.MUTATION_RATE)
        selection = Selection(self.selection_method)
        local_search = LocalSearch(self.time_set, self.shortest_path_dict)
        result = {'best_individual': None, 'best_fitness': None, 'best_distance': None, 'best_time_span': None,
                  'work_tp_count': [], 'fitness': [],
                  }
        fitness_values = Fitness.get_fitness_list(population, self.shortest_path_dict, self.time_set)
        elite_size = int(self.POPULATION_SIZE * self.ELITISM_RATE)

        pbar = tqdm(total=self.GENERATION_SIZE)
        # 진화 시작
        for generation in range(self.GENERATION_SIZE):
            data_test(population, self.BLOCKS)
            # 엘리트 개체 선택

            elites = [copy.deepcopy(population[i]) for i in np.argsort(fitness_values)[::-1][:elite_size]]

            # 자식 해 생성
            crossover_size = self.POPULATION_SIZE - elite_size
            offspring = Crossover.cross(crossover_size, fitness_values, population, self.transporter_container,
                                        selection, self.BLOCKS)

            # 돌연 변이 연산 수행
            mutation.apply_mutation(offspring, generation, self.GENERATION_SIZE)

            # 다음 세대 개체 집단 생성
            population = elites + offspring

            # 지역 탐색 연산 수행
            local_search.do_search(population)

            # 각 개체의 적합도 계산
            fitness_values = Fitness.get_fitness_list(population, self.shortest_path_dict, self.time_set)

            # 현재 세대에서 가장 우수한 개체 출력
            best_fitness, best_transporter_count, best_individual = self.get_best_solution(fitness_values, population)
            total_time = Fitness.individual_time_span(best_individual, self.time_set, self.shortest_path_dict)

            result["fitness"].append(fitness_values)
            result['work_tp_count'].append(best_transporter_count)
            pbar.set_description(desc="Hybrid Genetic Algorithm Run")
            pbar.set_postfix({'Best Transporter Count': best_transporter_count, 'Total Times:': total_time, 'Fitness': f'{best_fitness:.5f}'})
            pbar.update(1)

            data_test(population, self.BLOCKS)
        pbar.close()

        # 최종 세대에서 가장 우수한 개체 출력
        fitness_values = Fitness.get_fitness_list(population, self.shortest_path_dict, self.time_set)

        # 스케줄러 실행
        best_individual = population[np.argmax(fitness_values)]
        before_distance = round(Fitness.individual_distance(best_individual, self.shortest_path_dict), 3)
        before_time_span = round(Fitness.individual_time_span(best_individual, self.time_set, self.shortest_path_dict))
        before_fitness = Fitness.fitness(best_individual, self.time_set, self.shortest_path_dict)
        self.run_schedule_ga(best_individual)

        # 거리, 적합도 계산
        after_distance = round(Fitness.individual_distance(best_individual, self.shortest_path_dict), 3)
        after_time_span = round(Fitness.individual_time_span(best_individual, self.time_set, self.shortest_path_dict))
        after_fitness = Fitness.fitness(best_individual, self.time_set, self.shortest_path_dict)
        print(f'Scheduler reduced distances: {before_distance} -> {after_distance}')
        print(f'Scheduler reduced times: {before_time_span} -> {after_time_span}')
        print(f'Fitness Changes: {before_fitness} -> {after_fitness}')

        # 딕셔너리에 추가
        result['best_individual'] = best_individual
        result['best_fitness'] = Fitness.fitness(best_individual, self.time_set, self.shortest_path_dict)
        result['best_distance'] = Fitness.individual_distance(best_individual, self.shortest_path_dict)
        result['best_time_span'] = Fitness.individual_time_span(best_individual, self.time_set, self.shortest_path_dict)
        return result

    def run_schedule_ga(self, individual):
        for tp in tqdm(individual, desc="Scheduler Run"):
            works_len = len(tp.works)
            if works_len > 10:
                max_generation = 1000
                works = ScheduleGA(tp.works, self.shortest_path_dict, self.time_set, tp, population_size=100,
                                   max_generation=max_generation).run()
                tp.works = works
            elif 1 < works_len <= 10:
                max_generation = 100
                works = ScheduleGA(tp.works, self.shortest_path_dict, self.time_set, tp, population_size=100,
                                   max_generation=max_generation).run()
                tp.works = works


def print_tp(individual):
    for i in individual:
        if i.works:
            print("no: ", i.no, "available_weight: ", i.available_weight, "works_len: ", len(i.works))


if __name__ == "__main__":
    filemanager = FileManager()
    graph = Graph(node_file_path)
    transporter_container = filemanager.load_transporters(transporter_path)
    block_container = filemanager.load_block_data(block_path, BLOCK_NUM=precondition['BLOCKS'])

    ga = HGA(transporter_container, block_container, graph, ga_params, precondition)
    result = ga.run_GA()

    data = result['fitness']

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