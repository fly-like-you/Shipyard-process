from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.GA_refactoring.Mutation import Mutation
from transporter.transporter.GA_refactoring.Selection import Selection
from transporter.transporter.GA_refactoring.Population import Population
from transporter.transporter.GA_refactoring.Fitness import Fitness
from transporter.transporter.GA_refactoring.Crossover import Crossover
from transporter.transporter.GA_schedule.ScheduleGA import ScheduleGA
from transporter.transporter.create_data.Graph import Graph
import numpy as np
import pickle
import time
import os

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

node_file_path = os.path.join(os.getcwd(), '..', "create_data", "data","node(cluster3).csv")
transporter_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'transporter.csv')
block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'Blocks.csv')


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

class GA:
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

        return best_fitness, best_transporter_count

    def calc_simility(self, individual, individual2):
        def find_most_similar_set(target_set, other_sets): #
            max_jaccard_sim = 0

            for other_set in other_sets:
                union = len(target_set | other_set)
                jaccard_sim = len(target_set & other_set) / union if union != 0 else 0
                if jaccard_sim > max_jaccard_sim:
                    max_jaccard_sim = jaccard_sim

            return max_jaccard_sim

        tp_job_set_list = []
        tp_job_set_list2 = []
        score = 0
        for tp_idx in range(100):
            tp_job_set_list.append(set(block.no for block in individual[tp_idx].works))
            tp_job_set_list2.append(set(block.no for block in individual2[tp_idx].works))

        for target_set in tp_job_set_list:
            max_jaccard_sim = find_most_similar_set(target_set, tp_job_set_list2)
            score += max_jaccard_sim
        return score



    def run_GA(self):
        population = self.population.get_population()
        mutation = Mutation(self.MUTATION_RATE)
        selection = Selection(self.selection_method)
        result = {'best_individual': None, 'best_fitness': None, 'work_tp_count': [], 'fitness': [], 'similarity': []}
        fitness_values = Fitness.get_fitness_list(population, self.shortest_path_dict, time_set=self.time_set)
        prev_best_individual = population[np.argsort(fitness_values)[0]]
        # self.run_schedule_ga(population)
        # 진화 시작
        for generation in range(self.GENERATION_SIZE):

            # 엘리트 개체 선택
            elite_size = int(self.POPULATION_SIZE * self.ELITISM_RATE)
            elites = [population[i] for i in np.argsort(fitness_values)[::-1][:elite_size]]
            # 자식 해 생성
            crossover_size = self.POPULATION_SIZE - elite_size
            offspring = Crossover.cross(crossover_size, fitness_values, population, self.transporter_container, selection, self.BLOCKS)

            # 돌연 변이 연산 수행
            mutation.apply_mutation(offspring, generation, self.GENERATION_SIZE)

            # if generation % 250 == 0:
            #     self.run_schedule_ga(offspring)
            # 다음 세대 개체 집단 생성
            population = elites + offspring

            # 각 개체의 적합도 계산
            fitness_values = Fitness.get_fitness_list(population, self.shortest_path_dict, time_set=self.time_set)
            sorted_fit_val = sorted(fitness_values)


            # 현재 세대에서 가장 우수한 개체 출력
            best_individual, best_transporter_count = self.get_best_solution(fitness_values, population)

            len_fit = len(set(fitness_values))
            print(f'Generation {generation + 1} best individual: {best_transporter_count}, best_fitness_value: {np.max(fitness_values)}, overlap_fit:{self.POPULATION_SIZE - len_fit}, fitness:{sorted_fit_val[-5:]}')
            result['similarity'].append(self.calc_simility(prev_best_individual, population[np.argsort(fitness_values)[0]]))
            result["fitness"].append(fitness_values)
            result['work_tp_count'].append(best_transporter_count)
            # data_test(population, self.BLOCKS)


        # 최종 세대에서 가장 우수한 개체 출력
        fitness_values = Fitness.get_fitness_list(population, self.shortest_path_dict, time_set=self.time_set)
        best_individual = population[np.argmax(fitness_values)]
        print(
            f'Final generation best individual: {result["work_tp_count"][-1]}, best_fitness_value: {np.max(fitness_values)}, ')

        result['best_individual'] = best_individual
        result['best_fitness'] = Fitness.fitness(best_individual, self.time_set, self.shortest_path_dict)
        print('done')
        return result

    def run_schedule_ga(self, population):
        start_time = time.time()
        for individual in population:
            for transporter in individual:
                if len(transporter.works) > 5:
                    scheduling = ScheduleGA(transporter.works, self.shortest_path_dict, population_size=30,
                                            max_generation=200)
                    transporter.works = scheduling.run()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Parallel optimization took {elapsed_time:.2f} seconds.")


def print_tp(individual):
    for i in individual:
        if i.works:
            print("no: ", i.no, "available_weight: ", i.available_weight, "works_len: ", len(i.works))


if __name__ == "__main__":
    filemanager = FileManager()
    graph = Graph(node_file_path)
    transporter_container = filemanager.load_transporters(transporter_path)
    block_container = filemanager.create_block_from_graph_file(node_file_path, precondition['BLOCKS'])


    ga = GA(transporter_container, block_container, graph, ga_params, precondition)
    result = ga.run_GA()

    # with open(f'pickle_data/ga_result_mu_rate_{ga_params["MUTATION_RATE"]}.pkl', 'wb') as f:
    #     pickle.dump(result, f)

    tp = result['best_individual']
    tp.sort(key=lambda x: x.available_weight * x.work_speed, reverse=True)
    print_tp(tp)

