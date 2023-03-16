import os
import random

import numpy as np

from transporter.transporter.GA_schedule.Crossover import Crossover
from transporter.transporter.GA_schedule.Selection import Selection
from transporter.transporter.GA_schedule.Mutation import Mutation
from transporter.transporter.create_data.Block import Block
from transporter.transporter.create_data.Graph import Graph

class ScheduleGA:
    def __init__(self, blocks, shortest_path_dict, population_size=10, max_generation=100, elitism_rate=0.3, mutation_rate=0.2):
        self.blocks = blocks
        self.shortest_path_dict = shortest_path_dict
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
        prev_result = 0

        for generation in range(self.max_generation):
            selection = Selection(self.population, self.block_dict, self.shortest_path_dict)
            crossover = Crossover(selection, 1)
            # 적합도 평가
            fitness_values = selection.fitness_values
            best_fitness, best_solution = self.get_best_solution(fitness_values)

            # 결과 출력
            best_distance = int(1 / best_fitness)
            if prev_result != best_distance:
                prev_result = best_distance
                print(f'Generation {generation + 1} best individual: {best_solution}, best_distance: {best_distance}')

            # 엘리트 선택
            elite_size = int(self.population_size * self.elitism_rate)
            elites = [self.population[i] for i in np.argsort(fitness_values)[::-1][:elite_size]]

            # 교차
            offspring_size = self.population_size - elite_size
            offsprings = crossover.crossover(offspring_size)

            # 변이
            mutation.mutation(offsprings)

            # 엘리트 및 변이자를 포함하여 새로운 집단 생성
            self.population = elites + offsprings

        # 최종 해 선택
        best_fitness, best_solution = self.get_best_solution(fitness_values)
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

        return best_fitness, best_solution_idx


if __name__ == '__main__':
    node_file_path = os.path.join(os.getcwd(), "..", "create_data", "data", "node.csv")
    graph = Graph(node_file_path)
    shortest_path_dict = graph.get_shortest_path_dict()
    blocks = []
    for i in range(10):
        rand1, rand2 = random.sample([i for i in range(1, 31)], k=2)
        block = Block(i + 1, 1, rand1, rand2, 1, 1)
        blocks.append(block)

    ga = ScheduleGA(blocks, shortest_path_dict, population_size=100, max_generation=1000)
    sol = ga.run()
    print(sol)

# [3, 8, 9, 5, 6, 1, 2, 7, 10, 4] 21134