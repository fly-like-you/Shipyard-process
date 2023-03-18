import random
import numpy as np



class Selection:
    def __init__(self, method='roulette'):
        self.method = method

    def select(self, population, fitness_values):
        if self.method == 'roulette':
            return self.roulette_selection(population, fitness_values)
        elif self.method == 'selection2':
            return self.selection2(population, fitness_values)
        else:
            raise ValueError(f"Invalid selection method: {self.method}")


    def roulette_selection(self, population, fitness_values):
        cumulative_prob = self.get_cumulative_prob(fitness_values)
        parents = self.choice_parents(cumulative_prob, population)
        return parents

    def get_cumulative_prob(self, fitness_values):
        total_fitness = sum(fitness_values)
        probabilities = [f / total_fitness for f in fitness_values]
        cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        return cumulative_prob

    def choice_parents(self, cumulative_prob, population):
        parents = set()

        while len(parents) < 2:
            rand = random.random()
            for i in range(len(cumulative_prob)):
                if rand <= cumulative_prob[i]:
                    parents.add(tuple(population[i]))
                    break
        return parents
    def selection2(self, population, fitness_values, k=3):
          # 선택압 파라미터 k가 낮음수록 다양성이 높아짐

        max_fitness = max(fitness_values)
        min_fitness = min(fitness_values)
        # 적합도 계산
        fitness_calculated = []
        for fitness in fitness_values:
            fitness_calculated.append((fitness - min_fitness) + (max_fitness - min_fitness) / (k - 1))

        # 적합도 합계 계산
        fitness_sum = sum(fitness_calculated)

        # 룰렛휠 선택
        selected = set()
        while len(selected) < 2:
            point = random.uniform(0, fitness_sum)
            cumulative_prob = 0
            for j in range(len(fitness_calculated)):
                cumulative_prob += fitness_calculated[j]
                if cumulative_prob >= point:
                    selected.add(tuple(population[j]))
                    break
        return selected



if __name__ == '__main__':
    pass