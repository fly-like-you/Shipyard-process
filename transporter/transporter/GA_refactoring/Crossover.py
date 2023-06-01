import random
from transporter.transporter.GA_refactoring.Selection import Selection
from transporter.transporter.CustomDeepCopy import CustomDeepCopy

class SetSizeException(Exception):
    pass


class Crossover:
    @staticmethod
    def cross(crossover_size, fitness_values, population, empty_transporters, selection: Selection, block_count):
        # 교차 연산 수행
        offspring = []
        while len(offspring) < crossover_size:
            # 부모 개체 선택 이거 select함수에서 2개 뽑자
            parents = selection.select(population, fitness_values)
            parent1, parent2 = random.sample(parents, k=2)

            # 교차 연산 수행
            child1 = Crossover.crossover(parent1, parent2, empty_transporters, block_count)
            child2 = Crossover.crossover(parent1, parent2, empty_transporters, block_count)

            # 교차 연산 결과 자손 개체 추가
            if child1:
                offspring.append(child1)
            if child2 and len(offspring) < crossover_size:
                offspring.append(child2)

        return offspring

    @staticmethod
    def crossover(parent1, parent2, empty_transporters, block_count):
        def is_block_in_works(works, block_no):
            for idx, block in enumerate(works):
                if block.no == block_no:
                    return idx
            return -1

        child = CustomDeepCopy(empty_transporters).get_deep_copy()
        for tp in child:
            tp.works = [None for _ in range(block_count)]


        for i in range(1, block_count + 1):
            selected_parent = parent1 if random.random() < 0.5 else parent2

            for tp_idx, transporter in enumerate(selected_parent):
                b_idx = is_block_in_works(transporter.works, i)
                if b_idx == -1:
                    continue

                j = b_idx
                while j < len(child[tp_idx].works) and child[tp_idx].works[j] is not None:
                    j += 1

                if j < len(child[tp_idx].works):
                    child[tp_idx].works[j] = transporter.works[b_idx]
                else:
                    child[tp_idx].works.append(transporter.works[b_idx])

                break

        for tp in child:
            tp.works = [i for i in tp.works if i is not None]

        return child

