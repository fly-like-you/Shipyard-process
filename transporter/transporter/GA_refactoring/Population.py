import random
import copy

from transporter.transporter.GA_refactoring.Fitness import Fitness


class Population:
    def __init__(self, transporter_container, block_container, population_size):
        self.transporter_container = transporter_container
        self.block_container = block_container
        self.population_size = population_size
        self.population = []

    def get_population(self):
        return self.population

    def generate_population(self, time_set, shortest_path_dict):
        print("초기 해집단 생성")
        count = 1
        while len(self.population) < self.population_size:
            cur_population = copy.deepcopy(self.transporter_container)

            self.load_block_to_transporter(cur_population)

            if Fitness.fitness(cur_population, time_set, shortest_path_dict) > 0:
                print(f'{count}번째 해 생성')
                count += 1
                self.population.append(cur_population)



    def load_block_to_transporter(self, cur_population):
        for block in self.block_container:
            transporter_candidates = [t for t in cur_population if t.available_weight >= block.weight]

            transporter = transporter_candidates.pop(random.randint(0, len(transporter_candidates) - 1))
            transporter.works.insert(random.randint(0, len(transporter.works)), block)
            cur_population[transporter.no].works = transporter.works
