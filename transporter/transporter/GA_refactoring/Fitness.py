import math


class Fitness:
    # TODO 블록 맵 데이터를 그래프로 마이그레이션하기

    @staticmethod
    def fitness(individual, time_set):
        start_time = time_set['start_time']
        end_time = time_set['end_time']
        load_rest_time = time_set['load_rest_time']
        total_time = 0  # 모든 트랜스포터가 일을 마치는 시간을 계산
        DOCK = [0, 0]
        fitness_score = 0
        empty_tp_score = 1000
        for transporter in individual:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                return 0.0

        for transporter in individual:
            cur_time = start_time  # 작업을 시작할 수 있는 가장 빠른 시간
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
                cur_time += load_rest_time

            total_time = max(total_time, cur_time)  # 모든 트랜스포터가 일을 마치는 시간 업데이트

        fitness_score += 1 / total_time * 1

        if total_time > end_time:  # 전체 작업 완료 시간이 18시를 초과하면 해당 해는 유효하지 않음
            return 0.0

        return fitness_score  # 전체 작업 완료 시간의 역수를 반환하여 적합도 계산

    @staticmethod
    def get_fitness_list(population, time_set):
        return [Fitness.fitness(p, time_set) for p in population]