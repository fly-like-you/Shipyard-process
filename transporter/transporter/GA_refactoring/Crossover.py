import random
import copy
from transporter.transporter.GA_refactoring.Selection import Selection
from transporter.transporter.CustomDeepCopy import CustomDeepCopy
from transporter.transporter.GA_refactoring.Fitness import Fitness
from transporter.transporter.create_data.Graph import Graph
import os

node_file_path = os.path.join(os.getcwd(), '..', "create_data", "data", "node.csv")

time_set = {
    'start_time': 9,
    'end_time': 18,
    'load_rest_time': 0.3,
}
graph = Graph(node_file_path)
shortest_path_dict = graph.get_shortest_path_dict()
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
            if Fitness.fitness(child1, time_set, shortest_path_dict) == 0 or Fitness.fitness(child2, time_set, shortest_path_dict) == 0:
                continue

            # 교차 연산 결과 자손 개체 추가
            if child1:
                offspring.append(child1)
            if child2 and len(offspring) < crossover_size:
                offspring.append(child2)
        return offspring

    @staticmethod
    def crossover(parent1, parent2, empty_transporters, block_count):
        child1 = CustomDeepCopy(empty_transporters).get_deep_copy()
        child2 = CustomDeepCopy(empty_transporters).get_deep_copy()

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
