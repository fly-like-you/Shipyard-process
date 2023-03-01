import random
import numpy as np


class Selection:
    def __init__(self, method='roulette'):
        self.method = method

    def select(self, population, fitness_values):
        if self.method == 'roulette':
            return self.roulette_selection(population, fitness_values)
        elif self.method == 'tournament':
            return self.tournament_selection(population, fitness_values)
        elif self.method == 'sqrt_roulette':
            return self.sqrt_roulette_selection(population, fitness_values)
        elif self.method == 'square_roulette':
            return self.square_roulette_selection(population, fitness_values)
        elif self.method == 'scaled_roulette':
            return self.scaled_roulette_selection(population, fitness_values)
        else:
            raise ValueError(f"Invalid selection method: {self.method}")

    def roulette_selection(self, population, fitness_values):
        total_fitness = sum(fitness_values)

        probabilities = [f / total_fitness for f in fitness_values]
        cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        parents = self.choice_parents(cumulative_prob, population)
        return parents

    def tournament_selection(self, population, fitness_values, tournament_size=20):
        winners = set()

        while len(winners) < len(population) // 10:
            participants = random.sample(population, tournament_size)
            winner = max(participants, key=lambda x: fitness_values[population.index(x)])
            winners.add(tuple(winner))

        return winners

    # 임시
    def sqrt_roulette_selection(self, population, fitness_values):
        total_fitness = sum(fitness_values)

        probabilities = [f / total_fitness for f in fitness_values]

        cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        sqrt_cumulative_prob = np.sqrt(cumulative_prob)

        parents = self.choice_parents(sqrt_cumulative_prob, population)
        return parents

    # 임시
    def square_roulette_selection(self, population, fitness_values):
        total_fitness = sum(fitness_values)

        probabilities = [f / total_fitness for f in fitness_values]

        cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        sqrt_cumulative_prob = np.square(cumulative_prob)

        parents = self.choice_parents(sqrt_cumulative_prob, population)
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



    def choice_parents(self, cumulative_prob, population):
        parents = set()

        while len(parents) < len(population) // 10:
            rand = random.random()
            for i in range(len(cumulative_prob)):
                if rand <= cumulative_prob[i]:
                    parents.add(tuple(population[i]))
                    break
        return parents
