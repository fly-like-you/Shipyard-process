from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.GA_refactoring.Mutation import Mutation
from transporter.transporter.GA_refactoring.Selection import Selection
from transporter.transporter.GA_refactoring.Population import Population
from transporter.transporter.GA_refactoring.Fitness import Fitness
from transporter.transporter.GA_refactoring.Crossover import Crossover

import numpy as np
import os

config_dict = {
    'POPULATION_SIZE': 100,
    'GENERATION_SIZE': 200,
    'LOAD_REST_TIME': 0.2,
    'ELITISM_RATE': 0.4,
    'MUTATION_RATE': 0.3,
    'START_TIME': 9,
    'FINISH_TIME': 18,
    'BLOCKS': 100,
}
transporter_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'transporter.csv')
block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'blocks.csv')


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
                block_overlap_set.add(block)

    # then
    if len(block_overlap_set) != blocks:
        raise SetSizeException(f"Set size is not 30! generation")

class GA:
    def __init__(self, transport_container, block_container, config_dict, selection_method='roulette'):
        self.transport_container = transport_container
        self.block_container = block_container
        self.POPULATION_SIZE = config_dict['POPULATION_SIZE']
        self.GENERATION_SIZE = config_dict['GENERATION_SIZE']
        self.ELITISM_RATE = config_dict['ELITISM_RATE']
        self.MUTATION_RATE = config_dict['MUTATION_RATE']
        self.BLOCKS = config_dict['BLOCKS']

        self.time_set = {
            'start_time': config_dict['START_TIME'],
            'end_time': config_dict['FINISH_TIME'],
            'load_rest_time': config_dict['LOAD_REST_TIME'],
        }
        self.selection_method = selection_method
        self.population = Population(transporter_container, block_container, self.POPULATION_SIZE)
        self.population.generate_population(time_set=self.time_set)

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

        return best_fitness, best_transporter_count

    def run_GA(self):
        prev_transporter_count = 0
        population = self.population.get_population()
        mutation = Mutation(self.MUTATION_RATE)
        selection = Selection(self.selection_method)
        result = {'best_individual': None, 'work_tp_count': [], 'overlap_fit_val_len': []}

        fitness_values = Fitness.get_fitness_list(population, time_set=self.time_set)

        # 진화 시작
        for generation in range(self.GENERATION_SIZE):

            # 엘리트 개체 선택
            elite_size = int(self.POPULATION_SIZE * self.ELITISM_RATE)
            elites = [population[i] for i in np.argsort(fitness_values)[::-1][:elite_size]]

            # 자식 해 생성
            crossover_size = self.POPULATION_SIZE - elite_size
            offspring = Crossover.cross(crossover_size, fitness_values, population, self.transport_container, selection, self.BLOCKS)

            # 돌연 변이 연산 수행
            mutation.apply_mutation(offspring)

            # 다음 세대 개체 집단 생성
            population = elites + offspring

            # 각 개체의 적합도 계산
            fitness_values = Fitness.get_fitness_list(population, time_set=self.time_set)
            overlap_fitness_len = len(set(fitness_values))

            # 현재 세대에서 가장 우수한 개체 출력
            best_individual, best_transporter_count = self.get_best_solution(fitness_values, population)

            if best_transporter_count != prev_transporter_count:
                prev_transporter_count = best_transporter_count
                print(f'Generation {generation + 1} best individual: {best_transporter_count}, best_fitness_value: {np.max(fitness_values)}, len: {overlap_fitness_len}')

            result["overlap_fit_val_len"].append(overlap_fitness_len)
            result['work_tp_count'].append(best_transporter_count)
            data_test(population, self.BLOCKS)

        # 최종 세대에서 가장 우수한 개체 출력
        fitness_values = Fitness.get_fitness_list(population, time_set=self.time_set)
        best_individual = population[np.argmax(fitness_values)]
        print(
            f'Final generation best individual: {result["work_tp_count"][-1]}, best_fitness_value: {np.max(fitness_values)}, len:{result["overlap_fit_val_len"][-1]}')

        result['best_individual'] = best_individual
        return result




def print_tp(individual):
    for i in individual:
        if i.works:
            print("no: ", i.no, "available_weight: ", i.available_weight, "works_len: ", len(i.works))


if __name__ == "__main__":
    filemanager = FileManager()

    transporter_container = filemanager.load_transporters(transporter_path)
    block_container = filemanager.load_block_data(block_path, 100)

    ga = GA(transporter_container, block_container, config_dict, selection_method='square_roulette')
    tp = ga.run_GA()['best_individual']
    tp.sort(key=lambda x: x.available_weight * x.work_speed, reverse=True)
    print_tp(tp)
