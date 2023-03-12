import random

from transporter.transporter.GA_schedule.Selection import Selection
from transporter.transporter.create_data.Block import Block


class Crossover:
    def __init__(self, selection: Selection, crossover_rate=1):
        self.crossover_rate = crossover_rate
        self.selection = selection

    def crossover(self, crossover_size):
        offspring_pool = []
        while len(offspring_pool) < crossover_size:
            parent_1, parent_2 = self.selection.selection()
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
    # Block 인스턴스 3개 생성
    block1 = Block(1, 5, 10, 20, 0, 2, [0, 0], [0, 0])
    block2 = Block(2, 5, 20, 30, 2, 4, [3, 0], [3, 0])
    block3 = Block(3, 5, 30, 40, 4, 6, [3, 4], [3, 4])
    block4 = Block(4, 5, 30, 40, 4, 6, [2, 1], [3, 4])

    # 인스턴스 리스트 생성
    blocks = [block1, block2, block3]

    # 적합도 함수 테스트
    population1 = [[block1.no, block2.no, block3.no, block4.no], [block2.no, block1.no, block3.no, block4.no],
                   [block1.no, block2.no, block3.no, block4.no]]

