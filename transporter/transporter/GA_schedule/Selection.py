import random

class Selection:
    def __init__(self, population, block_dict: dict, shortest_path_dict, time_set, transporter):
        self.population = population
        self.shortest_path_dict = shortest_path_dict
        self.fitness_values = [self.__evaluate_fitness_(individual, block_dict, time_set, transporter) for individual in self.population]


    def __evaluate_fitness(self, individual, block_dict):
        total_distance = 0
        transporter_node = 1

        for block_no in individual:
            block = block_dict[block_no]
            total_distance += self.shortest_path_dict[block.start_node][block.end_node] + self.shortest_path_dict[transporter_node][block.start_node]
            transporter_node = block.end_node

        return 1 / total_distance

    def __evaluate_fitness_(self, individual, block_dict, time_set, transporter): # 블록의 작업 시간을 고려한 성능 평가
        start_time = time_set['start_time']
        end_time = time_set['end_time']
        load_rest_time = time_set['load_rest_time']

        total_distance = 0
        cur_time = start_time
        cur_node = 1

        for block_no in individual:
            block = block_dict[block_no]

            dist = self.shortest_path_dict[cur_node][block.start_node] / 1000  # 이전 위치에서 현재 블록까지 이동한 거리
            cur_time += dist / transporter.empty_speed  # 이동 시간 추가

            cur_time = max(cur_time, block.start_time)  # 블록의 작업 시작 시간 이전에 도착한 경우, 해당 시간까지 대기
            process_dist = self.shortest_path_dict[block.start_node][block.end_node] / 1000 # 운송 거리
            cur_time += process_dist / transporter.work_speed

            if block.end_time <= cur_time:
                total_distance *= 2

            cur_time += load_rest_time
            cur_node = block.end_node
            total_distance += process_dist + dist

        if cur_time >= end_time:  # 전체 작업 완료 시간이 18시를 초과하면 해당 해는 유효하지 않음
            total_distance *= 2

        return 1 / total_distance

    def selection2(self):
        k = 3  # 선택압 파라미터 k

        if len(set(self.fitness_values)) == 1:
            return random.sample(self.population, k=2)

        max_fitness = max(self.fitness_values)
        min_fitness = min(self.fitness_values)
        # 적합도 계산
        fitness_calculated = []
        for fitness in self.fitness_values:
            fitness_calculated.append((fitness - min_fitness) + (max_fitness - min_fitness) / (k - 1))


        # 적합도 합계 계산
        fitness_sum = sum(fitness_calculated)

        # 룰렛휠 선택
        selected = set()
        while len(selected) < 2:
            point = random.uniform(0, fitness_sum)
            cumulative_prob = 0
            for j in range(len(fitness_calculated)):
                cumulative_prob += fitness_calculated[j]
                if cumulative_prob >= point:
                    selected.add(tuple(self.population[j]))
                    break

        selected = list(selected)
        return list(selected[0]), list(selected[1])


if __name__ == '__main__':
    pass
