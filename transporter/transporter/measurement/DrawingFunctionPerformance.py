import time
import matplotlib.pyplot as plt

from transporter.transporter.GA_legacy import fitness
import time
import matplotlib.pyplot as plt


class DrawingFunctionPerformance:
    def __init__(self, func1, func2, args1, args2, num_trials):
        self.func1 = func1
        self.func2 = func2
        self.args1 = args1
        self.args2 = args2
        self.num_trials = num_trials
        self.times1, self.results1 = self.time_functions(self.func1, self.args1)
        self.times2, self.results2 = self.time_functions(self.func2, self.args2)
        self.fig, (self.ax1, self.ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))


    def time_functions(self, func, args):
        times = []
        results = []
        for i in range(self.num_trials):
            start = time.time()
            result = func(*args)
            end = time.time()
            times.append(end - start)
            results.append(result)
        return times, results

    def draw_time_graph(self):
        x = range(self.num_trials)
        self.ax1.plot(x, self.times1, color='b', label='Function 1')
        self.ax1.plot(x, self.times2, color='m', label='Function 2')
        self.ax1.set_xlabel('Iteration')
        self.ax1.set_ylabel('Execution time (s)')
        self.ax1.legend(loc='upper right')

    def draw_performance_graph(self):
        fitness_value1 = [fitness(individual) for individual in self.results1]
        fitness_value2 = [fitness(individual) for individual in self.results2]

        x = range(self.num_trials)
        self.ax2.plot(x, fitness_value1, color='b', label='Function 1')
        self.ax2.plot(x, fitness_value2, color='m', label='Function 2')
        self.ax2.set_xlabel('Iteration')
        self.ax2.set_ylabel('value time (s)')

    def show(self):
        plt.show()


