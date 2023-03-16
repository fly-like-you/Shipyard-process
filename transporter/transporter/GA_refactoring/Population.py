import random
import copy

from transporter.transporter.GA_refactoring.Fitness import Fitness
from transporter.transporter.CustomDeepCopy import CustomDeepCopy


class Population:
    def __init__(self, transporter_container, block_container, population_size):
        self.transporter_container = transporter_container
        self.block_container = block_container
        self.population_size = population_size
        self.population = []
        self.population = [CustomDeepCopy(self.transporter_container).get_deep_copy() for _ in range(self.population_size)]

    def get_population(self):
        return self.population

    def generate_population(self, time_set, shortest_path_dict):
        print("초기 해집단 생성")
        count = 1
        for individual in self.population:
            self.load_block_to_transporter(individual)
            print(f'{count}번째 해 생성')
            count += 1
            while True:
                fitness = Fitness.fitness(individual, time_set, shortest_path_dict)
                if fitness > 0:
                    break
                else:
                    for transporter in individual:
                        transporter.works.clear()
                    self.load_block_to_transporter(individual)


    def load_block_to_transporter(self, cur_population):
        for block in self.block_container:
            transporter_candidates = [t for t in cur_population if t.available_weight >= block.weight]

            transporter = transporter_candidates.pop(random.randint(0, len(transporter_candidates) - 1))
            transporter.works.insert(random.randint(0, len(transporter.works)), block)
            cur_population[transporter.no].works = transporter.works
