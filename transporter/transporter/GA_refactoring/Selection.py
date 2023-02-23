import random


class Selection:
    def __init__(self, method='roulette'):
        self.method = method

    def select(self, population, fitness_values):
        if self.method == 'roulette':
            return self.roulette_selection(population, fitness_values)
        elif self.method == 'tournament':
            return self.tournament_selection(population, fitness_values)
        else:
            raise ValueError(f"Invalid selection method: {self.method}")

    def roulette_selection(self, population, fitness_values):
        parents = []
        total_fitness = sum(fitness_values)

        probabilities = [f / total_fitness for f in fitness_values]
        cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        for _ in range(len(population)):
            rand = random.random()
            for i in range(len(cumulative_prob)):
                if rand <= cumulative_prob[i]:
                    parents.append(population[i])
                    break
        return parents

    def tournament_selection(self, population, fitness_values, tournament_size=2):
        winners = []
        for i in range(len(population)):
            participants = random.sample(population, tournament_size)
            winner = max(participants, key=lambda x: fitness_values[population.index(x)])
            winners.append(winner)
        return winners