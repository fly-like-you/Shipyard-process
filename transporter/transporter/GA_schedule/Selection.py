import random
import math
import numpy as np


class Selection:
    def __init__(self, population, block_dict):
        self.population = population
        self.block_dict = block_dict
        self.fitness_values = [self.evaluate_fitness(individual) for individual in self.population]

    def selection(self):
        square_cumulative_prob = self.get_cumulative_prob()
        parent_1, parent_2 = self.choice_parents(square_cumulative_prob)

        return parent_1, parent_2

    def get_cumulative_prob(self):
        total_fitness = sum(self.fitness_values)
        probabilities = [f / total_fitness for f in self.fitness_values]
        cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        square_cumulative_prob = np.square(cumulative_prob)
        return square_cumulative_prob



    def choice_parents(self, cumulative_prob):
        if self.population.count(self.population[0]) == len(self.population):
            return random.sample(self.population, k=2)

        parents = set()

        while len(parents) < 2:
            rand = random.random()
            for i in range(len(cumulative_prob)):
                if rand <= cumulative_prob[i]:
                    parents.add(tuple(self.population[i]))
                    break

        parents = list(parents)
        return list(parents[0]), list(parents[1])

    def evaluate_fitness(self, individual):
        total_distance = 0
        transporter_pos = [0, 0]

        for block_no in individual:
            block = self.block_dict[block_no]
            total_distance += math.dist(transporter_pos, block.start_pos) + math.dist(block.start_pos, block.end_pos)
            transporter_pos = block.end_pos

        return 1 / total_distance

if __name__ == '__main__':
    pass
