import multiprocessing
import queue
import time
from transporter.transporter.GA_schedule.ScheduleGA import ScheduleGA


class ParellelOptimizer:
    def __init__(self, population, shortest_path_dict):
        self.population = population
        self.shortest_path_dict = shortest_path_dict

    def optimize_transporter(self, population, execution_time_queue):
        start_time = time.time()

        for individual in population:
            for transporter in individual:
                if len(transporter.works) >= 4:
                    scheduling = ScheduleGA(transporter.works, self.shortest_path_dict, population_size=30, max_generation=100)
                    transporter.works = scheduling.run()

        end_time = time.time()
        execution_time = end_time - start_time
        execution_time_queue.put((execution_time, population))

    def run(self):
        processes = []
        populations = []
        task = int(len(self.population) * (1 / 10))
        first = task * 5
        second = first + task * 3

        populations.append(self.population[:first])
        populations.append(self.population[first:second])
        populations.append(self.population[second:])
        execution_time_queues = [multiprocessing.Queue() for _ in range(len(populations))]

        for i, population in enumerate(populations):
            p = multiprocessing.Process(target=self.optimize_transporter,
                                        args=(population, execution_time_queues[i]))
            p.start()
            processes.append(p)

        execution_times_and_populations = []
        while len(execution_times_and_populations) < len(processes):
            for q in execution_time_queues:
                try:
                    item = q.get_nowait()
                    execution_times_and_populations.append(item)
                except queue.Empty:
                    pass
                time.sleep(0.1)

        # 큐에서 가져온 population을 원래의 population에 대체합니다.
        index = 0
        for execution_time, modified_population in execution_times_and_populations:
            self.population[index:index+len(modified_population)] = modified_population
            index += len(modified_population)

        for p in processes:
            p.join()

