import random
from transporter.transporter.GA_refactoring.Fitness import Fitness

class LocalSearch:
    def __init__(self, time_set, shortest_path_dict):
        self.time_set = time_set
        self.shortest_path_dict = shortest_path_dict

    def do_search(self, population: list):

        # 인구 중에서 개별적으로 지역 탐색을 실행
        for individual in population:
            self.local_search(individual)


    def local_search(self, individual):
        # 지역 탐색 함수
        cur_individual_fitness = Fitness.fitness(individual, self.time_set, self.shortest_path_dict)

        transporter_li = [t for t in individual if len(t.works) > 0]
        transporter_li.sort(key=lambda t: len(t.works))


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