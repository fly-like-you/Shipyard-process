import random


class Mutation:
    def __init__(self, mutation_rate):
        self.mutation_rate = mutation_rate

    def mutation1(self, individual):
        pass

    def mutation2(self, individual):
        pass

    def apply_mutation(self, population):
        for individual in population:
            if random.random() < self.mutation_rate:
                # mutation1 or mutation2
                pass
