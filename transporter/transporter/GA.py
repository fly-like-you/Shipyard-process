import copy
import sys
import os
import math
from create_data.block import blocks  # 블록, 트랜스포터 정보 가져오기
from create_data.transporter import transporters
import random
import heapq
import itertools


def evaluation(arr):
    '''
        if arr이 실현가능한 해:
            return 운반에 걸리는 총 시간 (True를 의미)
        else return False
    '''
    if len(arr.works) == 0: # 트랜스포터의 작업이 0인 경우
        return True
    times = []
    for i in range(len(arr.works)): # 트랜스포터의 작업 수 만큼 반복
        if i == 0:
            prev = [0, 0]
            pick_up_time = arr.works[0].start_time
        else: # ???
            prev = arr.works[i - 1].end_pos
            pick_up_time = max(times[-1][1], arr.works[i].start_time)

        prev_to_start_dist = math.dist(prev, arr.works[i].start_pos) / 1000
        start_to_end_dist = math.dist(arr.works[i].start_pos, arr.works[i].end_pos) / 1000

        prev_to_start_time = prev_to_start_dist / arr.empty_speed
        start_to_end_time = start_to_end_dist / arr.work_speed
        finish_time = pick_up_time + prev_to_start_time + start_to_end_time

        flag = True
        for start, end in times:
            if not (pick_up_time >= end or finish_time <= start) or \
                    finish_time > 18 or \
                    arr.works[i].end_time < finish_time or \
                    finish_time + 0.5 > 18:
                flag = False
                break
        if flag:
            times.append([pick_up_time, finish_time + 0.5])
        else:
            return False

    total_time = 0
    for start, end in times:
        total_time += end - start
    return total_time


def generate_population(size):
    '''
        size 크기의 초기 세대를 생성
    '''
    ret = []
    for _ in range(size):
        cur_population = copy.deepcopy(transporters)
        for block in blocks:
            candidates = [] # 해당 블록에 대해 운반가능한 트랜스포터 후보
            for t in cur_population:
                if t.available_weight >= block.weight:
                    candidates.append(t)

            # 후보군에 대해서 evaluation이 참이면 해당 블록을 넣음
            while candidates:
                trans = candidates.pop(random.randint(0, len(candidates) - 1))
                temp_trans = copy.deepcopy(trans)
                temp_trans.works.insert(random.randint(0, max(1, len(temp_trans.works) - 1)), block) # 트랜스포터의 작업에 해당 블록을 랜덤하게 집어넣음
                if evaluation(temp_trans):
                    cur_population[temp_trans.no].works = temp_trans.works[::]
                    break
        ret.append(cur_population)
    return ret


population = generate_population(1)

def mutation_1():
    '''
        - muatation 1
        랜덤한 트랜스포터 2개 선택, 두 개의 트랜스포터를 스왑
    '''

    def mutation1_is_valid(cur_idx, swap_idx):  # cur, swap 트랜스포터의 작업들이 스왑 가능한지
        cur = population[0][cur_idx]
        swap = population[0][swap_idx]
        for work in cur.works:
            if work.weight > swap.available_weight:
                return False
        for work in swap.works:
            if work.weight > cur.available_weight:
                return False

        # cur 트랜스포터의 작업들을 swap트랜스포터에 적재 가능한지
        times = []
        for i in range(len(cur.works)):
            if i == 0:
                prev = [0, 0]
                pick_up_time = cur.works[i].start_time
            else:
                prev = cur.works[i - 1].end_pos
                pick_up_time = max(times[i - 1][1], cur.works[i].start_time)

            prev_to_start_dist = math.dist(prev, cur.works[i].start_pos) / 1000
            start_to_end_dist = math.dist(cur.works[i].start_pos, cur.works[i].end_pos) / 1000

            prev_to_start_time = prev_to_start_dist / swap.empty_speed
            start_to_end_time = start_to_end_dist / swap.work_speed
            finish_time = pick_up_time + prev_to_start_time + start_to_end_time

            flag = True
            for start, end in times:
                if not (pick_up_time >= end or finish_time <= start) or finish_time > 18 \
                        or cur.works[i].end_time < finish_time:
                    flag = False
                    break
            if flag:
                times.append([pick_up_time, finish_time + 0.5])
            else:
                return False

        # swap 트랜스포터의 작업들을 cur 트랜스포터에 적재 가능한지
        times = []
        for i in range(len(swap.works)):
            if i == 0:
                prev = [0, 0]
                pick_up_time = swap.works[i].start_time
            else:
                prev = swap.works[i - 1].end_pos
                pick_up_time = max(times[i - 1][1], swap.works[i].start_time)

            prev_to_start_dist = math.dist(prev, swap.works[i].start_pos) / 1000
            start_to_end_dist = math.dist(swap.works[i].start_pos, swap.works[i].end_pos) / 1000

            prev_to_start_time = prev_to_start_dist / cur.empty_speed
            start_to_end_time = start_to_end_dist / cur.work_speed
            finish_time = pick_up_time + prev_to_start_time + start_to_end_time

            flag = True
            for start, end in times:
                if not (pick_up_time >= end or finish_time <= start) or finish_time > 18 \
                        or swap.works[i].end_time < finish_time:
                    flag = False
                    break
            if flag:
                times.append([pick_up_time, finish_time + 0.5])
            else:
                return False

        population[0][cur_idx].works, population[0][swap_idx].works = population[0][swap_idx].works, population[0][
            cur_idx].works
        return True

    while True:
        cur_idx = random.randint(0, len(population[0]) - 1)
        swap_idx = random.randint(0, len(population[0]) - 1)
        if cur_idx == swap_idx or (len(population[0][cur_idx].works) == 0 and len(population[0][swap_idx].works) == 0):
            continue
        if mutation1_is_valid(cur_idx, swap_idx):
            temp = copy.deepcopy(population[0][cur_idx].works)
            population[0][cur_idx].works = copy.deepcopy(population[0][swap_idx].works)
            population[0][swap_idx].works = copy.deepcopy(temp)
            break


def mutation_2():
    '''
        - mutation2
        같은 트랜스포터 내에서 2개의 작업을 swap
    '''
    while True:
        idx = random.randint(0, len(population[0]) - 1)
        if len(population[0][idx].works) < 2:
            continue

        x, y = random.sample(range(len(population[0][idx].works)), 2)
        temp = copy.deepcopy(population[0][idx])
        temp.works[x], temp.works[y] = temp.works[x], temp.works[y]

        if evaluation(temp):
            population[0][idx].works = copy.deepcopy(temp.works)
            break


def mutation_3():
    '''
        - mutation3
        할당된 작업 수가 적은 트랜스포터 선택, 작업 많은 트랜스포터에 할당 함

        1. 할당된 작업 수가 가장 적은 트랜스포터 선택 (min_len 변수 이용)
        2. 할당된 작업 수가 가장 많은 트랜스포터 선택 (max_len 변수 이용)
        3. min_len 트랜스포터의 작업을 한개 랜덤 pop, max_len 트랜스포터에 랜덤 위치에 insert
        4. 실현 가능한 해인지 확인
    '''
    global population
    min_len = 1
    while min_len < 20:
        for min_len_trans in population[0]:
            if min_len == len(min_len_trans.works):
                max_len = max([len(x.works) for x in population[0]])
                while max_len:
                    for max_len_trans in population[0]:
                        if max_len == len(max_len_trans.works):
                            min_len_temp = copy.deepcopy(min_len_trans)  # 작업 적은 트랜스포터
                            max_len_temp = copy.deepcopy(max_len_trans)  # 작업 많은 트랜스포터
                            insert_block = min_len_temp.works.pop(random.randint(0, len(min_len_temp.works) - 1))
                            max_len_temp.works.insert(random.randint(0, len(max_len_temp.works) - 1), insert_block)
                            if evaluation(min_len_temp) and evaluation(max_len_temp):
                                population[0][min_len_trans.no].works = min_len_temp.works[::]
                                population[0][max_len_trans.no].works = max_len_temp.works[::]
                                return
                    max_len -= 1
        min_len += 1


# random으로 생성된 스케줄의 결과 확인
cnt = 0
time = 0
for i in population[0]:
    if i.works:
        cnt += 1
        time += evaluation(i)
print('random: ', cnt, time)

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
    if rand < 0.33:
        mutation_1()
    elif rand < 0.66:
        mutation_2()
    else:
        mutation_3()

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

'''
    트랜스포터의 대수를 줄이기 위한 휴리스틱
    유전 알고리즘 이후에 한 트랜스포터에 할당된 모든 작업들을
    다른 트랜스포터들에 할당 가능한지 확인해 트랜스포터의 대수를 줄인다.
'''


def can_insert(i, cur_block):
    for j, move_trans in enumerate(temp):
        if move_trans.works and i != j:
            for k in range(len(move_trans.works) + 1):
                temp[j].works.insert(k, cur_block)
                if evaluation(temp[j]):
                    return True
                else:
                    temp[j].works.pop(k)
    return False


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

'''
    트랜스포터에 할당된 작업들의 순서를 바꾸어, 트랜스포터의 이동거리를 최소화 하기 위한 알고리즘
    가지치기 기법을 통해 실현 불가능한 해는 더 이상 탐색하지 않으며
    20만회 이상 탐색할 경우 early stopping 방법을 통해 조기종료
'''


def perm(idx, length, arr):  # 순열, 백트래킹
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

cnt = 0
time = 0
for i in result_population:
    if i.works:
        cnt += 1
        time += evaluation(i)
print('최종 결과:', cnt, time)