import random
import math
import numpy as np


class Selection:
    def __init__(self, population, block_dict: dict, shortest_path_dict):
        self.population = population
        self.shortest_path_dict = shortest_path_dict
        self.fitness_values = [self.__evaluate_fitness(individual, block_dict) for individual in self.population]


    def __evaluate_fitness(self, individual, block_dict):
        total_distance = 0
        transporter_node = 1


        for block_no in individual:
            block = block_dict[block_no]
            total_distance += self.shortest_path_dict[block.start_node][block.end_node] + self.shortest_path_dict[transporter_node][block.start_node]
            transporter_node = block.end_node

        return 1 / total_distance

    def selection2(self):
        k = 5  # 선택압 파라미터 k

        if len(set(self.fitness_values)) == 1:
            return random.sample(self.population, k=2)

        max_fitness = max(self.fitness_values)
        min_fitness = min(self.fitness_values)
        # 적합도 계산
        fitness_calculated = []
        for fitness in self.fitness_values:
            fitness_calculated.append((fitness - min_fitness) + (max_fitness - min_fitness) / (k - 1))


        # 적합도 합계 계산
        fitness_sum = sum(fitness_calculated)

        # 룰렛휠 선택
        selected = set()
        while len(selected) < 2:
            point = random.uniform(0, fitness_sum)
            cumulative_prob = 0
            for j in range(len(fitness_calculated)):
                cumulative_prob += fitness_calculated[j]
                if cumulative_prob >= point:
                    selected.add(tuple(self.population[j]))
                    break

        selected = list(selected)
        return list(selected[0]), list(selected[1])


if __name__ == '__main__':
    pass
