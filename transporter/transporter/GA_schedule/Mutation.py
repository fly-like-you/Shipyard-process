import random


class Mutation:
    def __init__(self, probability):
        self.probability = probability

    def mutation(self, offsprings):
        for offspring in offsprings:
            if random.random() < self.probability:
                start_idx, end_idx = sorted(random.sample(range(len(offspring)), 2))

                scramble_genes = offspring[start_idx:end_idx + 1]
                random.shuffle(scramble_genes)
                offspring[start_idx:end_idx + 1] = scramble_genes

