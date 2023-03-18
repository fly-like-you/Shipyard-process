from transporter.transporter.GA_refactoring.Population import Population
from transporter.transporter.GA_schedule.ScheduleGA import ScheduleGA
from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.create_data.Graph import Graph
from transporter.transporter.GA_refactoring.Fitness import Fitness
import os

node_file_path = os.path.join(os.getcwd(), '..', "create_data", "data", "node.csv")
transporter_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'transporter.csv')
block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'Blocks.csv')

class MultiStart:
    def __init__(self, transporter_container, block_container, graph, size, time_set):
        self.transporter_container = transporter_container
        self.block_container = block_container
        self.graph = graph
        self.size = size
        self.shortest_path_dict = graph.get_shortest_path_dict()
        self.time_set = time_set
        self.fitness_values = None


    def run(self):
        population = Population(self.transporter_container, self.block_container, self.size)
        population.generate_population()
        population = population.get_population()

        self.fitness_values = Fitness.get_fitness_list(population, self.shortest_path_dict, self.time_set)





if __name__ == "__main__":
    config_dict = {
        'POPULATION_SIZE': 100,
        'GENERATION_SIZE': 1000,
        'LOAD_REST_TIME': 0.3,
        'ELITISM_RATE': 0.3,
        'MUTATION_RATE': 0.2,
        'START_TIME': 9,
        'FINISH_TIME': 18,
        'BLOCKS': 100,
    }
    time_set = {
        'start_time': config_dict['START_TIME'],
        'end_time': config_dict['FINISH_TIME'],
        'load_rest_time': config_dict['LOAD_REST_TIME'],
    }

    filemanager = FileManager()

    graph = Graph(node_file_path)
    transporter_container = filemanager.load_transporters(transporter_path)
    block_container = filemanager.load_block_data(block_path, 100)

    multi_start = MultiStart(transporter_container, block_container, graph, 100,time_set)
    multi_start.run()
    print( multi_start.fitness_values)





