import math
from scipy.stats import norm


class Fitness:
    @staticmethod
    def individual_time_span(individual, time_set, shortest_path_dict):
        start_time = time_set['start_time']
        load_rest_time = time_set['load_rest_time']

        total_time = 0  # 모든 트랜스포터가 일을 마치는 시간을 계산
        DOCK = 1  # 트랜스포터 시작 노드

        for transporter in individual:
            cur_time = start_time  # 작업을 시작할 수 있는 가장 빠른 시간
            cur_node = DOCK  # 현재 위치는 도크

            for block in transporter.works:
                dist = shortest_path_dict[cur_node][block.start_node] / 1000  # 이전 위치에서 현재 블록까지 이동한 거리
                cur_time += dist / transporter.empty_speed  # 이동 시간 추가

                cur_time = max(cur_time, block.start_time)  # 블록의 작업 시작 시간 이전에 도착한 경우, 해당 시간까지 대기
                span_time = (shortest_path_dict[block.start_node][block.end_node] / 1000) / transporter.work_speed

                cur_time += span_time + load_rest_time  # 블록을 운반하는데 걸리는 시간 추가
                cur_node = block.end_node  # 현재 위치를 블록의 종료 위치로 업데이트

            total_time += cur_time - start_time  # 모든 트랜스포터가 일을 마치는 시간 업데이트

        return total_time  # 전체 작업 완료 시간의 역수를 반환하여 적합도 계산


    @staticmethod
    def fitness(individual, time_set, shortest_path_dict, gaussian_list, log=False):
        def divide_integer_part(num, penalty):
            penalty += 1
            integer_part = int(num)
            decimal_part = num - integer_part

            result = (integer_part / penalty) + decimal_part
            return result

        start_time = time_set['start_time']
        end_time = time_set['end_time']
        load_rest_time = time_set['load_rest_time']
        total_time = 0  # 모든 트랜스포터가 일을 마치는 시간을 계산
        DOCK = 1  # 트랜스포터 시작 노드

        fitness_score = 0
        empty_tp_score = 0
        works_score = 0
        weight_score = 0
        work_time_factor = False
        transporter_weight_available_factor = False
        total_time_factor = False
        span_time_score = 0



        for idx, transporter in enumerate(individual):
            cur_time = start_time  # 작업을 시작할 수 있는 가장 빠른 시간
            cur_node = DOCK  # 현재 위치는 도크

            if not transporter.works:
                empty_tp_score += 1
                if transporter.available_weight > 500:
                    weight_score += 1

            else:
                num_works = len(transporter.works)
                works_score += gaussian_list[num_works]
            for block in transporter.works:
                dist = shortest_path_dict[cur_node][block.start_node] / 1000  # 이전 위치에서 현재 블록까지 이동한 거리
                cur_time += dist / transporter.empty_speed  # 이동 시간 추가

                cur_time = max(cur_time, block.start_time)  # 블록의 작업 시작 시간 이전에 도착한 경우, 해당 시간까지 대기
                cur_time += (shortest_path_dict[block.start_node][block.end_node] / 1000) / transporter.work_speed  # 블록을 운반하는데 걸리는 시간 추가
                if block.end_time <= cur_time:
                    work_time_factor = True

                cur_time += load_rest_time
                cur_node = block.end_node  # 현재 위치를 블록의 종료 위치로 업데이트
            span_time_score += cur_time - start_time
            total_time = max(total_time, cur_time)  # 모든 트랜스포터가 일을 마치는 시간 업데이트

        str_n = str(weight_score)
        str_n = '0' * (2 - len(str_n)) + str_n
        fitness_score += int(str(empty_tp_score) + str(int(works_score)) + str_n) + 1 / total_time
        for transporter in individual:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                transporter_weight_available_factor = True
                break

        if total_time >= end_time:  # 전체 작업 완료 시간이 18시를 초과하면 해당 해는 유효하지 않음
            total_time_factor = True

        penalty_factor = work_time_factor + total_time_factor + transporter_weight_available_factor * 5
        fitness_score = divide_integer_part(fitness_score, penalty_factor)
        if fitness_score >= 1000000:
            print(fitness_score)
            print(empty_tp_score, works_score, weight_score)
            raise Exception("계산 에러")

        if log:
            print(f"패널티 요소")
            print(f"work_time_factor: {work_time_factor}, total_time_factor: {total_time_factor}, transporter_weight_available_factor:{transporter_weight_available_factor}")
            print(empty_tp_score, works_score, weight_score)
        return fitness_score


    @staticmethod
    def get_fitness_list(population, shortest_path_dict, time_set, gaussian_list):
        return [Fitness.fitness(p, time_set, shortest_path_dict, gaussian_list) for p in population]

    @staticmethod
    def individual_distance(individual, shortest_path_dict):
        DOCK = 1  # 트랜스포터 시작 노드
        fitness_score = 0

        for transporter in individual:
            cur_node = DOCK  # 현재 위치는 도크

            for block in transporter.works:
                # 트랜스포터 위치 -> 블록 시작 위치
                load_to_block_dist = shortest_path_dict[cur_node][block.start_node] / 1000  # 이전 위치에서 현재 블록까지 이동한 거리
                # 블록 시작 위치 -> 블록 적재 위치
                block_delivery_dist = shortest_path_dict[block.start_node][block.end_node] / 1000
                fitness_score += load_to_block_dist + block_delivery_dist
                cur_node = block.end_node  # 현재 위치를 블록의 종료 위치로 업데이트

        return fitness_score


