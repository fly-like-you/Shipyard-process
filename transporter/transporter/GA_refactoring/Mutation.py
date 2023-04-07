import random
import math


class Mutation:
    def __init__(self, mutation_rate):
        self.mutation_rate = mutation_rate

    def mutation(self, individual):
        transporter_li = [t for t in individual if len(t.works) > 0]
        transporter_li.sort(key=lambda t: len(t.works))

        for tp_index in range(len(transporter_li) // 2):
        # for tp_index in range(1):
            min_len_trans, max_len_trans = random.sample(transporter_li[:5], k=2)

            if len(min_len_trans.works) > len(max_len_trans.works):
                min_len_trans, max_len_trans = max_len_trans, min_len_trans

            max_len_trans_index = individual.index(max_len_trans)
            min_len_trans_index = individual.index(min_len_trans)

            max_len_trans_works = individual[max_len_trans_index].works
            min_len_trans_works = individual[min_len_trans_index].works

            if not min_len_trans_works or not max_len_trans_works:
                continue
            insert_block = random.choice(min_len_trans_works)

            max_len_trans_works.insert(random.randint(0, len(max_len_trans_works) - 1), insert_block)
            individual[min_len_trans_index].works = [b for b in min_len_trans_works if b.no != insert_block.no]

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
        # mutation_rate = self.dynamic_mutation_rate(current_gen, generation)
        mutation_rate = self.mutation_rate
        for individual in population:
            if random.random() < mutation_rate:
                self.mutation(individual)
            if random.random() < mutation_rate:
                self.mutation2(individual)

    def dynamic_mutation_rate(self, current_gen, generation, alpha=2):
        progress = current_gen / generation
        adjusted_progress = math.pow(progress, alpha)
        return self.mutation_rate * (1 - adjusted_progress)
