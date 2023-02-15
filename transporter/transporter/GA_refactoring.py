# 새로 작성한 GA
import copy

from create_data.block import blocks  # 블록, 트랜스포터 정보 가져오기
from create_data.transporter import transporters
import random
import math
import numpy as np
from GA import evaluation

# 상수 정의
FINISH_TIME = 18
START_TIME = 9
LOAD_REST_TIME = 0.5
POPULATION_SIZE = 100  # 개체집단 크기
GENERATION_SIZE = 100  # 진화 세대 수
ELITISM_RATE = 0.1  # 엘리트 개체 비율
MUTATION_RATE = 0.2  # 돌연변이 확률


def generate_population(size, transporter_li, block_li):
    population = []
    for gen in range(size):
        cur_population = copy.deepcopy(transporter_li)
        for block in block_li:
            transporter_candidates = [t for t in cur_population if t.available_weight >= block.weight]

            # 시간적으로 알맞은 트랜스포터 작업 선정
            while transporter_candidates:
                transporter = transporter_candidates.pop(random.randint(0, len(transporter_candidates) - 1))
                transporter.works.insert(random.randint(0, len(transporter.works)), block)
                if evaluation(transporter):
                    cur_population[transporter.no].works = transporter.works
                    break
        population.append(cur_population)
    return population


def fitness(individual):
    total_time = 0  # 모든 트랜스포터가 일을 마치는 시간을 계산
    DOCK = [0, 0]
    fitness_score = 0
    empty_tp_score = 500

    for transporter in individual:
        cur_time = START_TIME  # 작업을 시작할 수 있는 가장 빠른 시간
        cur_pos = DOCK  # 현재 위치는 도크

        if not transporter.works:
            fitness_score += empty_tp_score

        for block in transporter.works:
            dist = math.dist(cur_pos, block.start_pos) / 1000  # 이전 위치에서 현재 블록까지 이동한 거리
            cur_time += dist / transporter.empty_speed  # 이동 시간 추가

            cur_time = max(cur_time, block.start_time)  # 블록의 작업 시작 시간 이전에 도착한 경우, 해당 시간까지 대기

            dist2 = math.dist(block.start_pos, block.end_pos) / 1000
            cur_time += dist2 / transporter.work_speed  # 블록을 운반하는데 걸리는 시간 추가

            cur_pos = block.end_pos  # 현재 위치를 블록의 종료 위치로 업데이트
        total_time = max(total_time, cur_time)  # 모든 트랜스포터가 일을 마치는 시간 업데이트

    fitness_score += total_time * 10

    if total_time > FINISH_TIME:  # 전체 작업 완료 시간이 18시를 초과하면 해당 해는 유효하지 않음
        return 0.0

    return fitness_score  # 전체 작업 완료 시간의 역수를 반환하여 적합도 계산


def selection(population, fitness_values):
    parents = []
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        probabilities = [1/len(fitness_values) for _ in range(len(fitness_values))]
    else:
        probabilities = [f / total_fitness for f in fitness_values]
    cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
    for _ in range(len(population)):
        rand = random.random()
        for i in range(len(cumulative_prob)):
            if rand <= cumulative_prob[i]:
                parents.append(population[i])
                break
    return parents



def crossover(parent1, parent2):
    child1 = copy.deepcopy(transporters)
    child2 = copy.deepcopy(transporters)
    for i in range(1, 101):
        # 각 부모 트랜스포터 중 하나 선택
        if random.random() < 0.5:
            selected_parent = parent1
            other_parent = parent2
        else:
            selected_parent = parent2
            other_parent = parent1

        # 선택한 부모 트랜스포터의 works 리스트에서 현재 블록 번호를 가진 블록 선택
        flag1 = False
        blok = []
        for idx, transporter in enumerate(selected_parent):
            for block in transporter.works:
                if block.no == i:
                    child1[idx].works.append(block)
                    blok.append(block)
                    flag1 = True
                    break
            if flag1:
                break

        # 다른 부모 트랜스포터의 works 리스트에서 중복되지 않는 블록 선택
        flag2 = False
        for idx, transporter in enumerate(other_parent):
            for block in transporter.works:
                if block.no == i and block not in blok:
                    child2[idx].works.append(block)
                    flag2 = True
                    break
                if flag1:
                    break
    return child1, child2


def run_GA():
    population = generate_population(POPULATION_SIZE, transporters, blocks)
    initial_len = 0
    li1 = []
    for i in population[0]:
        if i.works:
            initial_len += 1
            for j in i.works:
                li1.append(j.no)

    # 진화 시작
    for generation in range(GENERATION_SIZE):
        # 각 개체의 적합도 계산
        fitness_values = [fitness(p) for p in population]

        # 현재 세대에서 가장 우수한 개체 출력
        best_individual = population[np.argmin(fitness_values)]
        print(f'Generation {generation + 1} best individual: {best_individual}')

        # 엘리트 개체 선택
        elite_size = int(POPULATION_SIZE * ELITISM_RATE)
        elites = [population[i] for i in np.argsort(fitness_values)[:elite_size]]

        # 교차 연산 수행
        crossover_size = POPULATION_SIZE - elite_size
        offspring = []
        while len(offspring) < crossover_size:
            # 부모 개체 선택
            parents = selection(population, fitness_values)
            parent1, parent2 = random.sample(parents, k=2)

            # 교차 연산 수행
            child1, child2 = crossover(parent1, parent2)
            # 교차 연산 결과 자손 개체 추가
            if child1:
                offspring.append(child1)
            if child2 and len(offspring) < crossover_size:
                offspring.append(child2)
        # 돌연변이 연산 수행
        # for ind in offspring:
        #     mutation(ind, transporters, blocks, MUTATION_RATE)

        # 다음 세대 개체집단 생성
        population = elites + offspring

    # 최종 세대에서 가장 우수한 개체 출력
    fitness_values = [fitness(p) for p in population]
    best_individual = population[np.argmin(fitness_values)]
    print(f'Final generation best individual: {best_individual}')
    count = 0
    li = []
    for i in best_individual:
        if i.works:
            count += 1
            for j in i.works:
                li.append(j.no)

            print()
    li.sort()
    li1.sort()
    print("최초")
    print(li1)
    print(len(li1))
    print(initial_len)

    print("결과")
    print(li)
    print(len(li))
    print(count)



if __name__ == "__main__":
    run_GA()
