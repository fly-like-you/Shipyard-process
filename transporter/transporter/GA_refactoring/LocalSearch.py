import random
import copy
from transporter.transporter.GA_refactoring.Fitness import Fitness


class LocalSearch:
    def __init__(self, time_set, shortest_path_dict):
        self.time_set = time_set
        self.shortest_path_dict = shortest_path_dict

    def do_search(self, population: list):
        # 인구 중에서 개별적으로 지역 탐색을 실행
        for idx, individual in enumerate(population):
            population[idx] = self.local_search(individual)


    def local_search(self, individual):

        # 지역 탐색 함수
        cur_individual_fitness = Fitness.fitness(individual, self.time_set, self.shortest_path_dict)

        local_individual = copy.deepcopy(individual)

        transporter_li = [t for t in local_individual if len(t.works) > 0]
        transporter_li.sort(key=lambda t: len(t.works))

        min_len_trans, max_len_trans = random.sample(transporter_li[:15], k=2)

        if len(min_len_trans.works) > len(max_len_trans.works):
            min_len_trans, max_len_trans = max_len_trans, min_len_trans

        max_len_trans_index = local_individual.index(max_len_trans)
        min_len_trans_index = local_individual.index(min_len_trans)

        max_len_trans_works = local_individual[max_len_trans_index].works
        min_len_trans_works = local_individual[min_len_trans_index].works

        # 블록 하나만 교체
        insert_block = min_len_trans_works.pop(random.randint(0, len(min_len_trans_works) - 1))
        max_len_trans_works.insert(random.randint(0, len(max_len_trans_works) - 1), insert_block)


        local_search_fitness = Fitness.fitness(local_individual, self.time_set, self.shortest_path_dict)

        if local_search_fitness > cur_individual_fitness:
            return local_individual
        else:
            return individual
