import os
from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.GA_refactoring import GA


class Configuration:
    def __init__(self):
        self.block_container = self.create_blocks_from_node()
        self.transporter_container = self.read_transporters_from_file()

        self.finish_time = 18
        self.start_time = 9
        self.load_rest_time = 0.5
        self.population_size = 100  # 개체집단 크기
        self.generation_size = 100  # 진화 세대 수
        self.elitism_rate = 0.5  # 엘리트 개체 비율
        self.mutation_rate = 0.4  # 돌연변이 확률
        self.blocks = 100

    def create_blocks_from_node(self):
        file_manager = FileManager()
        block_path = os.path.join(os.getcwd(), 'create_data', 'data', 'map.xlsx')
        return file_manager.load_block_data(block_path, 100)

    def read_transporters_from_file(self):
        file_manager = FileManager()
        transporter_path = os.path.join(os.getcwd(), 'create_data', 'data', 'transporter.csv')
        return file_manager.get_transporters(transporter_path)

    def get_GA_config(self):
        return {
            'POPULATION_SIZE': self.population_size,
            'GENERATION_SIZE': self.generation_size,
            'LOAD_REST_TIME': self.load_rest_time,
            'ELITISM_RATE': self.elitism_rate,
            'MUTATION_RATE': self.mutation_rate,
            'START_TIME': self.start_time,
            'FINISH_TIME': self.finish_time,
            'BLOCKS': self.blocks,

        }


if __name__ == "__main__":
    config = Configuration()
    # print(config.transporters)
    # print(config.block_container)
    ga = GA(config.transporter_container, config.block_container, config.get_GA_config())
    ga.run_GA()
