import os
import random

import numpy as np

from transporter.transporter.GA_schedule.Crossover import Crossover
from transporter.transporter.GA_schedule.Selection import Selection
from transporter.transporter.GA_schedule.Mutation import Mutation
from transporter.data.create_data.Block import Block
from transporter.data.create_data.Transporter import Transporter
from transporter.data.create_data.Graph import Graph

import copy
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
class ScheduleGA:
    def __init__(self, blocks, shortest_path_dict, time_set, transporter, population_size=10, max_generation=100, elitism_rate=0.3, mutation_rate=0.2):
        self.blocks = blocks
        self.shortest_path_dict = shortest_path_dict
        self.time_set = time_set
        self.transporter = transporter
        self.population_size = population_size
        self.max_generation = max_generation
        self.elitism_rate = elitism_rate
        self.mutation_rate = mutation_rate
        self.block_dict = self.block_dict_init()
        self.population = self.init_population()

    def block_dict_init(self):
        block_dict = dict()
        for block in self.blocks:
            block_dict[block.no] = block
        return block_dict

    def run(self):
        mutation = Mutation(self.mutation_rate)

        for generation in range(self.max_generation):
            selection = Selection(self.population, self.block_dict, self.shortest_path_dict, self.time_set, self.transporter)
            crossover = Crossover(selection, 1)
            # 적합도 평가
            fitness_values = selection.fitness_values
            best_fitness, best_solution, best_solution_idx = self.get_best_solution(fitness_values)

            # 엘리트 선택
            elite_size = int(self.population_size * self.elitism_rate)
            elites = [copy.deepcopy(self.population[i]) for i in np.argsort(fitness_values)[::-1][:elite_size]]

            # 교차
            offspring_size = self.population_size - elite_size
            offsprings = crossover.crossover(offspring_size)

            # 변이
            mutation.mutation(offsprings)

            # 엘리트 및 변이자를 포함하여 새로운 집단 생성
            self.population = elites + offsprings

        # 최종 해 선택
        selection = Selection(self.population, self.block_dict, self.shortest_path_dict, self.time_set, self.transporter)
        fitness_values = selection.fitness_values
        best_fitness, best_solution, best_solution_idx = self.get_best_solution(fitness_values)

        return best_solution

    def init_population(self):
        population = []
        for i in range(self.population_size):
            pop_row = [block.no for block in self.blocks]
            random.shuffle(pop_row)
            population.append(pop_row)
        return population

    def get_best_solution(self, fitness_values):
        best_idx = np.argmax(fitness_values)
        best_fitness = fitness_values[best_idx]
        best_solution_idx = self.population[best_idx]
        best_solution = [self.block_dict[idx] for idx in best_solution_idx]

        return best_fitness, best_solution, best_solution_idx
cluster = 2
block = 100
data_path = os.path.join(get_dir_path("transporter"), "data")
node_file_path = os.path.join(data_path, "nodes_and_blocks", "cluster", "simply_mapping", str(cluster), f"node.csv")

if __name__ == '__main__':
    time_set = {
        'start_time': 9,
        'end_time': 18,
        'load_rest_time': 0.2
    }

    graph = Graph(node_file_path)
    shortest_path_dict = graph.get_shortest_path_dict()
    blocks = []
    for i in range(10):
        # start_time = random.randint(9, 11)
        start_time = 9
        # end_time = random.randint(11, 181)
        end_time = 18
        print(f"block: {i + 1} -> start_time: {start_time}, end_time: {end_time}")
        block = Block(i + 1, 1, i+1, i+2, start_time, end_time)
        blocks.append(block)

    transporter = Transporter(1, 500, 10, 5)
    result = []
    ga = ScheduleGA(blocks, shortest_path_dict, time_set, transporter, population_size=100, max_generation=1000)
    sol = ga.run()
    result.append(sol)
    print(result)

