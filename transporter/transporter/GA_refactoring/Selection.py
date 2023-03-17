import random
import numpy as np
from matplotlib import pyplot as plt


class Selection:
    def __init__(self, method='roulette'):
        self.method = method

    def select(self, population, fitness_values):
        if self.method == 'roulette':
            return self.roulette_selection(population, fitness_values)
        elif self.method == 'scaled_roulette':
            return self.scaled_roulette_selection(population, fitness_values)
        elif self.method == 'square_roulette':
            return self.square_roulette_selection(population, fitness_values)
        elif self.method == 'selection2':
            return self.selection2(population, fitness_values)
        else:
            raise ValueError(f"Invalid selection method: {self.method}")

    def square_roulette_selection(self, population, fitness_values):
        cumulative_prob = self.get_cumulative_prob(fitness_values)
        sqrt_cumulative_prob = np.square(cumulative_prob)

        parents = self.choice_parents(sqrt_cumulative_prob, population)
        return parents

    def roulette_selection(self, population, fitness_values):
        cumulative_prob = self.get_cumulative_prob(fitness_values)
        parents = self.choice_parents(cumulative_prob, population)
        return parents

    def scaled_roulette_selection(self, population, fitness_values):
        total_fitness = sum(fitness_values)

        # 스케일
        scale_factor = 1.7
        low_scale_factor = 0.3
        num_low = int(len(population) * 0.4)
        probabilities = [f / total_fitness for f in fitness_values]
        probabilities[:num_low] = [p * low_scale_factor for p in probabilities[:num_low]]
        probabilities[num_low:] = [p * scale_factor for p in probabilities[num_low:]]

        # 누적합에 맞춰서 정규화하기
        cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        normalization_factor = cumulative_prob[-1]
        cumulative_prob = [p / normalization_factor for p in cumulative_prob]

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

    def selection2(self, population, fitness_values, k=4):
        k = 5  # 선택압 파라미터 k

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