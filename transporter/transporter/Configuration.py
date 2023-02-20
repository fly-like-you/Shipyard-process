import os
from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.GA_refactoring import GA


class Configuration:
    def __init__(self, transporter_path, block_path, map_path=None):
        self.finish_time = 18
        self.start_time = 9
        self.load_rest_time = 0.5
        self.population_size = 100  # 개체집단 크기
        self.generation_size = 3000  # 진화 세대 수
        self.elitism_rate = 0.3  # 엘리트 개체 비율
        self.mutation_rate = 0.8  # 돌연변이 확률
        self.blocks = 100

        self.transporter_container = self.read_transporters_from_file(transporter_path)
        self.block_container = self.read_blocks_from_file(block_path)




    def create_blocks_from_node(self, map_path):
        if map_path:
            file_manager = FileManager()
            return file_manager.create_block_from_map_file(map_path, self.blocks)

    def read_transporters_from_file(self, transporter_path):
        file_manager = FileManager()
        return file_manager.load_transporters(transporter_path)

    def read_blocks_from_file(self, block_path):
        file_manager = FileManager()
        return file_manager.load_block_data(block_path)

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
    file_manager = FileManager()

    transporter_path = os.path.join(os.getcwd(), 'create_data', 'data', 'transporter.csv')
    block_path = os.path.join(os.getcwd(), 'create_data', 'data', 'blocks.csv')

    config = Configuration(transporter_path, block_path)

    transporter_container = file_manager.load_transporters(transporter_path)
    block_container = file_manager.load_block_data(block_path, 100)

    for i in block_container:
        print(i)
    ga = GA(config.transporter_container, config.block_container, config.get_GA_config())
    ga.run_GA()
