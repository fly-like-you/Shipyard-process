import random

from transporter.transporter.GA_schedule.Selection import Selection


class Crossover:
    def __init__(self, selection: Selection, crossover_rate=1):
        self.crossover_rate = crossover_rate
        self.selection = selection

    def crossover(self, crossover_size):
        offspring_pool = []
        while len(offspring_pool) < crossover_size:
            parent_1, parent_2 = self.selection.selection2()
            if random.random() < self.crossover_rate:
                child1 = self.__ordered_crossover(parent_1, parent_2)
            else:
                child1 = parent_1

            offspring_pool.append(child1)

        return offspring_pool

    def __ordered_crossover(self, parent_1, parent_2):
        length = len(parent_1)

        # 두 부모 중 임의로 두 개의 자름선을 정한다.
        cut_point_1 = random.randint(0, length - 1)
        cut_point_2 = random.randint(0, length - 1)

        # 두 자름선이 같으면 자식은 부모와 같아진다.
        if cut_point_1 == cut_point_2:
            return parent_1

        # 자름선이 더 큰 값에서 작은 값으로 정렬되도록 변경한다.
        if cut_point_1 > cut_point_2:
            cut_point_1, cut_point_2 = cut_point_2, cut_point_1

        # 첫 번째 자름선과 두 번째 자름선 사이의 부분을 복사한다.
        child = parent_1[cut_point_1:cut_point_2]

        # 남은 부분에 대해 두 번째 부모의 순서를 따라가며 복사한다.
        for gene in parent_2:
            if gene not in child:
                # 자식 해에 해당 유전자가 없다면 추가한다.
                child.append(gene)

        return child




if __name__ == '__main__':
    pass

