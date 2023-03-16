import random
import math


class Mutation:
    def __init__(self, mutation_rate):
        self.mutation_rate = mutation_rate

    def mutation(self, individual):
        transporter_li = [t for t in individual if len(t.works) > 0]
        transporter_li.sort(key=lambda t: len(t.works))

        for tp_index in range(len(transporter_li) // 2):
            min_len_trans = random.choice(transporter_li[:2])
            max_len_trans = random.choice(transporter_li[-8:])

            if min_len_trans == max_len_trans:
                continue
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
            small_tp_idx, large_tp_idx = random.sample(range(len(individual)), 2)

            # 선택된 두 요소의 값을 비교하여 작은 값이 j가 되도록 함
            if individual[small_tp_idx].available_weight * individual[small_tp_idx].work_speed > individual[
                large_tp_idx].available_weight * \
                    individual[large_tp_idx].work_speed:
                small_tp_idx, large_tp_idx = large_tp_idx, small_tp_idx

            small_tp = individual[small_tp_idx]
            large_tp = individual[large_tp_idx]
            if len(small_tp.works) > len(large_tp.works):
                # 선택된 두 트랜스포터의 작업 목록을 서로 스왑
                swap_transporter_works(small_tp, large_tp)

    def apply_mutation(self, population, current_gen, generation):
        mutation_rate = self.dynamic_mutation_rate(current_gen, generation)

        for individual in population:
            if random.random() < mutation_rate:
                self.mutation(individual)
            if random.random() < mutation_rate:
                self.mutation2(individual)


    def dynamic_mutation_rate(self, current_gen, generation, alpha=2):

        progress = current_gen / generation
        adjusted_progress = math.pow(progress, alpha)
        return self.mutation_rate * (1 - adjusted_progress)
