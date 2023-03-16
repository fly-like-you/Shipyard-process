import random
import copy
from transporter.transporter.GA_refactoring.Selection import Selection


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
            child1, child2 = Crossover.crossover(parent1, parent2, empty_transporters, block_count)
            # 교차 연산 결과 자손 개체 추가
            if child1:
                offspring.append(child1)
            if child2 and len(offspring) < crossover_size:
                offspring.append(child2)
        return offspring

    @staticmethod
    def crossover(parent1, parent2, empty_transporters, block_count):
        child1 = copy.deepcopy(empty_transporters)
        child2 = copy.deepcopy(empty_transporters)
        for i in range(1, block_count + 1):
            # 각 부모 트랜스포터 중 하나 선택
            if random.random() < 0.5:
                selected_parent = parent1
                other_parent = parent2
            else:
                selected_parent = parent2
                other_parent = parent1

            # 선택한 부모 트랜스포터의 works 리스트에서 현재 블록 번호를 가진 블록 선택
            flag1 = False
            for idx, transporter in enumerate(selected_parent):
                for block in transporter.works:
                    if block.no == i:
                        child1[idx].works.append(block)
                        flag1 = True
                        break
                if flag1:
                    break

            # 다른 부모 트랜스포터의 works 리스트에서 중복되지 않는 블록 선택
            flag2 = False
            for idx, transporter in enumerate(other_parent):
                for block in transporter.works:
                    if block.no == i:
                        child2[idx].works.append(block)
                        flag2 = True
                        break
                    if flag2:
                        break
        return child1, child2
