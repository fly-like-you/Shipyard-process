import random
import math


class Mutation:
    def __init__(self, mutation_rate):
        self.mutation_rate = mutation_rate

    def mutation(self, individual):
        for _ in range(len(individual)):
            rand_idx = random.randint(0, len(individual) - 1)

            works_len = len(individual[rand_idx].works)
            if works_len >= 2:
                random.shuffle(individual[rand_idx].works)

    def pop_mutation(self, individual):
        for _ in range(len(individual)):

            rand_idx1, rand_idx2 = random.sample(range(len(individual) - 1), 2)

            work_pop = individual[rand_idx1].works
            work_insert = individual[rand_idx1].works
            if work_pop:
                block = work_pop.pop(random.randint(0, len(work_pop) - 1))
                insert_idx = random.randint(0, len(work_insert) - 1) if len(work_insert) != 0 else 0
                work_insert.insert(insert_idx, block)




    def mutation2(self, individual):
        def swap_transporter_works(transporter1, transporter2):
            temp_works = transporter1.works
            transporter1.works = transporter2.works
            transporter2.works = temp_works

        for i in range(len(individual)):
            light_tp_idx, heavy_tp_idx = random.sample(range(len(individual)), 2)

            # 선택된 두 요소의 값을 비교하여 작은 값이 j가 되도록 함
            if individual[light_tp_idx].available_weight * individual[light_tp_idx].work_speed > \
                    individual[heavy_tp_idx].available_weight * individual[heavy_tp_idx].work_speed:
                light_tp_idx, heavy_tp_idx = heavy_tp_idx, light_tp_idx

            light_tp = individual[light_tp_idx]
            heavy_tp = individual[heavy_tp_idx]
            if len(light_tp.works) > len(heavy_tp.works):
                # 선택된 두 트랜스포터의 작업 목록을 서로 스왑
                swap_transporter_works(light_tp, heavy_tp)

    def apply_mutation(self, population, current_gen, generation):
        mutation_rate = self.mutation_rate
        for individual in population:
            if random.random() < mutation_rate:
                self.mutation(individual)
                self.pop_mutation(individual)
                # self.mutation2(individual)

