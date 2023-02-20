import os
import copy
import time
import math
import random
from transporter.transporter.GA_refactoring import GA
from transporter.transporter.create_data.FileManager import FileManager

# 상수 정의
FINISH_TIME = 18
START_TIME = 9
LOAD_REST_TIME = 0.5
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("Execution time of function '{}': {} seconds".format(func.__name__, end_time - start_time))
        return result
    return wrapper



def evaluation(transporter):
    '''
        if arr이 실현가능한 해:
            return 운반에 걸리는 총 시간 (True를 의미)
        else return False
    '''
    if len(transporter.works) == 0: # 트랜스포터의 작업이 0인 경우
        return True
    times = []
    for work_idx in range(len(transporter.works)): # 트랜스포터의 작업 수 만큼 반복
        if transporter.available_weight < transporter.works[work_idx].weight:
            return False
        if work_idx == 0:
            prev = [0, 0]
            pick_up_time = transporter.works[0].start_time
        else: # ???
            prev = transporter.works[work_idx - 1].end_pos
            pick_up_time = max(times[-1][1], transporter.works[work_idx].start_time) # 직전 작업과 비교하여 최대값 선정


        # 트랜스포터가 현재 지점에서 블록까지 가는 곳 까지의 거리
        prev_to_start_dist = math.dist(prev, transporter.works[work_idx].start_pos) / 1000
        # 블록이 이동될 거리
        start_to_end_dist = math.dist(transporter.works[work_idx].start_pos, transporter.works[work_idx].end_pos) / 1000

        prev_to_start_time = prev_to_start_dist / transporter.empty_speed
        start_to_end_time = start_to_end_dist / transporter.work_speed

        # 트랜스포터가 현재 위치에서 해당 블록을 목표지점까지 가져다 놓는데 걸리는 시간
        finish_time = pick_up_time + prev_to_start_time + start_to_end_time

        flag = True
        for start, end in times:
            # 안의 판별식이 모두 False이면 불가능한해이므로 리턴
            if not (pick_up_time >= end or finish_time <= start) or \
                    finish_time > FINISH_TIME or \
                    transporter.works[work_idx].end_time < finish_time or \
                    finish_time + LOAD_REST_TIME > FINISH_TIME:  #
                flag = False
                break
        if flag:
            times.append([pick_up_time, finish_time + LOAD_REST_TIME])
        else:
            return False

    total_time = 0
    for start, end in times:
        total_time += end - start
    return total_time



def generate_population(size, transporters, blocks):
    ret = []
    for _ in range(size):
        cur_population = copy.deepcopy(transporters)
        for block in blocks:
            transporter_candidates = [t for t in cur_population if t.available_weight >= block.weight]
            while transporter_candidates:
                transporter = transporter_candidates.pop(random.randint(0, len(transporter_candidates) - 1))
                temp_transporter = copy.deepcopy(transporter)
                temp_transporter.works.insert(random.randint(0, len(temp_transporter.works)), block)
                if evaluation(temp_transporter):
                    cur_population[transporter.no].works = temp_transporter.works
                    break
        ret.append(cur_population)
    return ret

def mutation_1():

    def is_valid_swap(cur_idx, swap_idx):
        cur_transporter = population[0][cur_idx]
        swap_transporter = population[0][swap_idx]
        for work in cur_transporter.works:
            if work.weight > swap_transporter.available_weight:
                return False
        for work in swap_transporter.works:
            if work.weight > cur_transporter.available_weight:
                return False

        times = []
        def is_valid_transporter(transporter):
            nonlocal times
            times = []
            for i in range(len(transporter.works)):
                if i == 0:
                    prev = [0, 0]
                    pick_up_time = transporter.works[i].start_time
                else:
                    prev = transporter.works[i - 1].end_pos
                    pick_up_time = max(times[i - 1][1], transporter.works[i].start_time)

                prev_to_start_dist = math.dist(prev, transporter.works[i].start_pos) / 1000
                start_to_end_dist = math.dist(transporter.works[i].start_pos, transporter.works[i].end_pos) / 1000

                prev_to_start_time = prev_to_start_dist / transporter.empty_speed
                start_to_end_time = start_to_end_dist / transporter.work_speed
                finish_time = pick_up_time + prev_to_start_time + start_to_end_time

                flag = True
                for start, end in times:
                    if not (pick_up_time >= end or finish_time <= start) or finish_time > 18 \
                            or transporter.works[i].end_time < finish_time:
                        flag = False
                        break
                if flag:
                    times.append([pick_up_time, finish_time + 0.5])
                else:
                    return False
            return True

        if is_valid_transporter(cur_transporter) and is_valid_transporter(swap_transporter):
            population[0][cur_idx].works, population[0][swap_idx].works = population[0][swap_idx].works, population[0][cur_idx].works
            return True

    while True:
        cur_idx = random.randint(0, len(population[0]) - 1)
        swap_idx = random.randint(0, len(population[0]) - 1)
        if cur_idx != swap_idx and is_valid_swap(cur_idx, swap_idx):
            break



def mutation_2():
    '''
        - mutation2
        같은 트랜스포터 내에서 2개의 작업을 swap
    '''
    while True:
        idx = random.randint(0, len(population[0]) - 1)
        transporter = population[0][idx]
        if len(transporter.works) < 2:
            continue

        work1, work2 = random.sample(transporter.works, 2)
        transporter.works.remove(work1)
        transporter.works.remove(work2)
        transporter.works.append(work1)
        transporter.works.append(work2)

        if evaluation(transporter):
            break





def mutation_3(mutationRate):

    transporters = copy.deepcopy(population[0])
    for tp_index in range(len(transporters) // 2):
        if random.random() < mutationRate:
            min_len_trans = min(transporters, key=lambda t: len(t.works))
            transporters.pop(transporters.index(min_len_trans))

            max_len_trans = max(transporters, key=lambda t: len(t.works))
            transporters.pop(transporters.index(max_len_trans))

            min_len_temp = copy.deepcopy(min_len_trans)
            max_len_temp = copy.deepcopy(max_len_trans)

            if len(min_len_temp.works) != 0:
                insert_block = min_len_temp.works.pop(random.randint(0, len(min_len_temp.works) - 1))
                max_len_temp.works.insert(random.randint(0, len(max_len_temp.works) - 1), insert_block)

            if evaluation(min_len_temp) and evaluation(max_len_temp):
                population[0][min_len_trans.no].works = min_len_temp.works[::]
                population[0][max_len_trans.no].works = max_len_temp.works[::]

def can_insert(i, cur_block):
    '''
        트랜스포터의 대수를 줄이기 위한 휴리스틱
        유전 알고리즘 이후에 한 트랜스포터에 할당된 모든 작업들을
        다른 트랜스포터들에 할당 가능한지 확인해 트랜스포터의 대수를 줄인다.
    '''
    for j, move_trans in enumerate(temp):
        if move_trans.works and i != j:
            for k in range(len(move_trans.works) + 1):
                temp[j].works.insert(k, cur_block)
                if evaluation(temp[j]):
                    return True
                else:
                    temp[j].works.pop(k)
    return False



def perm(idx, length, arr):  # 순열, 백트래킹
    '''
        트랜스포터에 할당된 작업들의 순서를 바꾸어, 트랜스포터의 이동거리를 최소화 하기 위한 알고리즘
        가지치기 기법을 통해 실현 불가능한 해는 더 이상 탐색하지 않으며
        20만회 이상 탐색할 경우 early stopping 방법을 통해 조기종료
    '''
    global cnt
    cnt += 1
    if cnt > 200000:
        return
    if idx == length:
        global min_dist
        dist = evaluation(arr)
        if min_dist > dist:  # 현재 route가 기존 dist보다 작은 경우, tsp_route갱신
            global tsp_route
            tsp_route = arr.works[::]
            min_dist = dist
        return

    for i in range(length):  # 순열 로직
        if not visited[i]:
            arr.works.append(trans.works[i])
            if evaluation(arr):
                visited[i] = True
                perm(idx + 1, length, arr)
                visited[i] = False
            arr.works.pop()
def fitness(individual):
    total_time = 0  # 모든 트랜스포터가 일을 마치는 시간을 계산
    DOCK = [0, 0]
    fitness_score = 0
    empty_tp_score = 100000
    for transporter in individual:
        if any(work.weight > transporter.available_weight for work in transporter.works):
            return 0.0

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

            if cur_time > block.end_time:  # 운반을 끝내는데 걸린 시간이 작업종료시간을 만족하지 않는다면 해는 유효하지 않음
                return 0.0
            cur_pos = block.end_pos  # 현재 위치를 블록의 종료 위치로 업데이트

        total_time = max(total_time, cur_time)  # 모든 트랜스포터가 일을 마치는 시간 업데이트

    fitness_score += total_time * 1

    if total_time > FINISH_TIME:  # 전체 작업 완료 시간이 18시를 초과하면 해당 해는 유효하지 않음
        return 0.0

    return fitness_score  # 전체 작업 완료 시간의 역수를 반환하여 적합도 계산
@measure_execution_time
def run_ga(transporters, blocks):
    global population, cnt, temp, flag, trans, min_dist, tsp_route, visited, arr
    population = generate_population(1, transporters, blocks)
    # random으로 생성된 스케줄의 결과 확인
    initital_count = 0
    initital_time = 0
    for i in population[0]:
        if i.works:
            initital_count += 1
            initital_time += evaluation(i)
    print('initiial fitness_value:', fitness(population[0]))
    print('random: ', initital_count, initital_time)
    '''
            GA
            각 mutation 연산은 1/3의 확률로 적용
            또한 500세대 mutation 연산 이후에도 최적해의 변화가 없으면 early stopping 방법을 통해 조기 종료 한다. 
        '''
    ans = [math.inf, math.inf]
    result_population = None
    best = 0
    stop = 0
    for i in range(1000):
        rand = random.random()
        if rand < 0.25:
            mutation_1()
        elif rand < 0.50:
            mutation_2()
        elif result_population is not None and rand < 0.75:
            for i, cur_trans in enumerate(result_population):
                if cur_trans.works:
                    temp = copy.deepcopy(result_population)
                    flag = True

                    while temp[i].works:
                        cur_block = temp[i].works.pop()
                        if not can_insert(i, cur_block):
                            flag = False
                            break

                    if flag:
                        result_population = copy.deepcopy(temp)
        else:
            mutation_3(0.9)



        # 매 세대마다 결과 측정
        cnt = 0
        time = 0
        for j in population[0]:
            if j.works:
                cnt += 1
                time += evaluation(j)

        if ans > [cnt, time]:
            ans = [cnt, time]
            result_population = copy.deepcopy(population[0])
            stop = 0

        # 똑같은 결과가 500세대가 되면, early stop
        stop += 1
        if stop == 500:
            break

    for i, cur_trans in enumerate(result_population):
        if cur_trans.works:
            temp = copy.deepcopy(result_population)
            flag = True

            while temp[i].works:
                cur_block = temp[i].works.pop()
                if not can_insert(i, cur_block):
                    flag = False
                    break

            if flag:
                result_population = copy.deepcopy(temp)
    for trans in result_population:
        if trans.works:
            min_dist = math.inf
            tsp_route = []
            visited = [False] * len(trans.works)
            arr = copy.deepcopy(trans)
            arr.works = []
            cnt = 0
            perm(0, len(trans.works), arr)
            trans.works = tsp_route[::]  # tsp_route를 현재 트랜스포터의 작업 순서로
    optimization_count = 0
    work = 0
    optimization_time = 0
    for i in result_population:
        if i.works:
            optimization_count += 1
            work += len(i.works)
            optimization_time += evaluation(i)
    print('best fitness_value:', fitness(result_population))

    print('최종 결과:', optimization_count, optimization_time, work)
    # given
    transporter_list = result_population
    performance = (abs(initital_count - optimization_count) / initital_count + abs(initital_time - optimization_time) / initital_time) * 100


    # for i in transporter_list:
    #     if i.works:
    #         print('transporter')
    #         print(i)
    #         print('blocks')
    #         for j in i.works:
    #             print(j)
    #
    #         print()

    return transporter_list, performance





if __name__ == '__main__':
    file_manager = FileManager()

    transporter_path = os.path.join(os.getcwd(), 'create_data', 'data', 'transporter.csv')
    block_path = os.path.join(os.getcwd(), 'create_data', 'data', 'blocks.csv')

    transporter_container = file_manager.load_transporters(transporter_path)
    block_container = file_manager.load_block_data(block_path, 100)

    for i in block_container:
        print(i)
    run_ga(transporter_container, block_container)

