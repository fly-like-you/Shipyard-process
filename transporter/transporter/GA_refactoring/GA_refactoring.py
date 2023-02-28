# 새로 작성한 GA
import copy
from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.GA_refactoring.Mutation import Mutation
from transporter.transporter.GA_refactoring.Selection import Selection
import random
import math
import numpy as np
import os

config_dict = {
    'POPULATION_SIZE': 100,
    'GENERATION_SIZE': 100,
    'LOAD_REST_TIME': 0.2,
    'ELITISM_RATE': 0.4,
    'MUTATION_RATE': 0.6,
    'START_TIME': 9,
    'FINISH_TIME': 18,
    'BLOCKS': 100,
}
transporter_path = os.path.join(os.getcwd(), 'create_data', 'data', 'transporter.csv')
block_path = os.path.join(os.getcwd(), 'create_data', 'data', 'map.xlsx')


class SetSizeException(Exception):
    pass


class GA:
    def __init__(self, transport_container, block_container, config_dict, selection_method='roulette'):
        self.transport_container = transport_container
        self.block_container = block_container
        self.POPULATION_SIZE = config_dict['POPULATION_SIZE']
        self.GENERATION_SIZE = config_dict['GENERATION_SIZE']
        self.LOAD_REST_TIME = config_dict['LOAD_REST_TIME']
        self.ELITISM_RATE = config_dict['ELITISM_RATE']
        self.MUTATION_RATE = config_dict['MUTATION_RATE']
        self.START_TIME = config_dict['START_TIME']
        self.FINISH_TIME = config_dict['FINISH_TIME']
        self.BLOCKS = config_dict['BLOCKS']

        self.selection_method = selection_method

    def generate_population(self, size, transporter_li, block_li):
        population = []

        while len(population) < size:
            cur_population = copy.deepcopy(transporter_li)

            for block in block_li:
                transporter_candidates = [t for t in cur_population if t.available_weight >= block.weight]

                transporter = transporter_candidates.pop(random.randint(0, len(transporter_candidates) - 1))
                transporter.works.insert(random.randint(0, len(transporter.works)), block)
                cur_population[transporter.no].works = transporter.works

            if self.fitness(cur_population) > 0:
                population.append(cur_population)
        return population

    def fitness(self, individual):
        total_time = 0  # 모든 트랜스포터가 일을 마치는 시간을 계산
        DOCK = [0, 0]
        fitness_score = 0
        empty_tp_score = 1000
        for transporter in individual:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                return 0.0

        for transporter in individual:
            cur_time = self.START_TIME  # 작업을 시작할 수 있는 가장 빠른 시간
            cur_pos = DOCK  # 현재 위치는 도크

            if not transporter.works:
                fitness_score += empty_tp_score
                if transporter.available_weight > 500:
                    fitness_score += empty_tp_score // 100

            for block in transporter.works:
                dist = math.dist(cur_pos, block.start_pos) / 1000  # 이전 위치에서 현재 블록까지 이동한 거리
                cur_time += dist / transporter.empty_speed  # 이동 시간 추가

                cur_time = max(cur_time, block.start_time)  # 블록의 작업 시작 시간 이전에 도착한 경우, 해당 시간까지 대기

                dist2 = math.dist(block.start_pos, block.end_pos) / 1000
                cur_time += dist2 / transporter.work_speed  # 블록을 운반하는데 걸리는 시간 추가

                if cur_time > block.end_time:  # 운반을 끝내는데 걸린 시간이 작업종료시간을 만족하지 않는다면 해는 유효하지 않음
                    return 0.0
                cur_pos = block.end_pos  # 현재 위치를 블록의 종료 위치로 업데이트
                cur_time += self.LOAD_REST_TIME

            total_time = max(total_time, cur_time)  # 모든 트랜스포터가 일을 마치는 시간 업데이트

        fitness_score += 1 / total_time * 1

        if total_time > self.FINISH_TIME:  # 전체 작업 완료 시간이 18시를 초과하면 해당 해는 유효하지 않음
            return 0.0

        return fitness_score  # 전체 작업 완료 시간의 역수를 반환하여 적합도 계산

    def crossover(self, parent1, parent2, empty_transporters):
        child1 = copy.deepcopy(empty_transporters)
        child2 = copy.deepcopy(empty_transporters)
        for i in range(1, self.BLOCKS + 1):
            # 각 부모 트랜스포터 중 하나 선택
            if random.random() < 0.5:
                selected_parent = parent1
                other_parent = parent2
            else:
                selected_parent = parent2
                other_parent = parent1

            # 선택한 부모 트랜스포터의 works 리스트에서 현재 블록 번호를 가진 블록 선택
            flag1 = False
            for idx, transporter in enumerate(selected_parent):
                for block in transporter.works:
                    if block.no == i:
                        child1[idx].works.append(block)
                        flag1 = True
                        break
                if flag1:
                    break

            # 다른 부모 트랜스포터의 works 리스트에서 중복되지 않는 블록 선택
            flag2 = False
            for idx, transporter in enumerate(other_parent):
                for block in transporter.works:
                    if block.no == i:
                        child2[idx].works.append(block)
                        flag2 = True
                        break
                    if flag2:
                        break
        return child1, child2

    def test_data(self, inspect_population):  # 블록 개수와 블록 중복 체크
        # given
        block_overlap_set = set()

        # when
        for transporter_list in inspect_population:
            for transporter in transporter_list:
                process = transporter.works

                for block in process:
                    block_overlap_set.add(block)

        # then
        if len(block_overlap_set) != self.BLOCKS:
            raise SetSizeException(f"Set size is not 30! generation")

    def test_tp_data(self, transporter_list):  # 블록 개수와 블록 중복 체크
        # given
        block_overlap_set = set()
        block_numbering = set(i + 1 for i in range(self.BLOCKS))
        # when
        for transporter in transporter_list:
            process = transporter.works

            for block in process:
                block_overlap_set.add(block.no)

        # then
        if len(block_overlap_set) != self.BLOCKS:
            print(block_numbering - block_overlap_set)
            raise SetSizeException(f"Set size is not 30! generation")

    def print_individual(self, individual):
        self.test_tp_data(individual)
        work_tp_count = 0
        for transporter in individual:
            if transporter.works:
                work_tp_count += 1
        return work_tp_count

    # 트랜스 포터의 대수는 5대 이상이어야함 (인덱스 오류뜸)

    def run_GA(self):
        mutation = Mutation(self.MUTATION_RATE)
        selection = Selection(self.selection_method)
        population = self.generate_population(self.POPULATION_SIZE, self.transport_container, self.block_container)
        work_tp_count_list = []
        overlap_fit_val_list = []
        # 진화 시작
        for generation in range(self.GENERATION_SIZE):
            # 각 개체의 적합도 계산
            fitness_values = [self.fitness(p) for p in population]
            overlap_fit_val_list.append(len(set(fitness_values)))

            # 현재 세대에서 가장 우수한 개체 출력
            best_individual = population[np.argmax(fitness_values)]
            work_tp_count_list.append(self.print_individual(best_individual))
            print(
                f'Generation {generation + 1} best individual: {work_tp_count_list[generation]}, best_fitness_value: {np.max(fitness_values)}')
            # 엘리트 개체 선택
            elite_size = int(self.POPULATION_SIZE * self.ELITISM_RATE)
            elites = [population[i] for i in np.argsort(fitness_values)[::-1][:elite_size]]
            self.test_data(elites)
            # 교차 연산 수행
            crossover_size = self.POPULATION_SIZE - elite_size
            offspring = []
            while len(offspring) < crossover_size:
                # 부모 개체 선택
                parents = selection.select(population, fitness_values)
                self.test_data(parents)
                parent1, parent2 = random.sample(parents, k=2)

                # 교차 연산 수행
                child1, child2 = self.crossover(parent1, parent2, self.transport_container)
                # 교차 연산 결과 자손 개체 추가
                if child1:
                    offspring.append(child1)
                if child2 and len(offspring) < crossover_size:
                    offspring.append(child2)
            mutation.apply_mutation(offspring)

            # 다음 세대 개체 집단 생성
            population = elites + offspring

            # 돌연 변이 연산 수행

        # 최종 세대에서 가장 우수한 개체 출력
        fitness_values = [self.fitness(p) for p in population]
        best_individual = population[np.argmax(fitness_values)]
        print(
            f'Final generation best individual: {work_tp_count_list[-1]}, best_fitness_value: {np.max(fitness_values)}')

        result = dict()
        result['best_individual'] = best_individual
        result['work_tp_count'] = work_tp_count_list
        result['overlap_fit_val_len'] = overlap_fit_val_list
        return result



def print_tp(individual):
    for i in individual:
        if i.works:
            print("no: ", i.no, "available_weight: ", i.available_weight, "works_len: ", len(i.works))

if __name__ == "__main__":
    filemanager = FileManager()

    transporter_container = filemanager.load_transporters(transporter_path)
    block_container = filemanager.create_block_from_map_file(block_path, 100)

    ga = GA(transporter_container, block_container, config_dict, selection_method='roulette')
    tp = ga.run_GA()['best_individual']
    tp.sort(key=lambda x: x.available_weight * x.work_speed, reverse=True)
    print_tp(tp)
