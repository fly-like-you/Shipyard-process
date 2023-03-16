import os
from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.GA_refactoring.GA_refactoring import GA

transporter_path = os.path.join(os.getcwd(), 'create_data', 'data', 'transporter.csv')
block_path = os.path.join(os.getcwd(), 'create_data', 'data', 'blocks.csv')

config_dict = {
    'POPULATION_SIZE': 100,  # 한 세대에서의 인구 수를 설정합니다.
    'GENERATION_SIZE': 100,  # 몇 세대에 걸쳐 진화할 지 설정합니다.
    'LOAD_REST_TIME': 0.5,  # 트랜스포터가 목적지에서 물건을 실어나르는 시간을 설정합니다 (시)
    'ELITISM_RATE': 0.3,  # 엘리트 individual의 비율을 결정합니다.
    'MUTATION_RATE': 0.3,  # 돌연변이가 일어날 확률을 설정합니다.
    'START_TIME': 9,  # 일과의 시작시간을 결정합니다.
    'FINISH_TIME': 18,  # 일과가 끝나는 시간을 결정합니다.
    'BLOCKS': 100,  # 총 블록 수를 설정합니다. 최대 100개까지 설정가능합니다.
}


class Configuration:
    def __init__(self, transporter_path, block_path, config_dict=config_dict, map_path=None, selection_method='roulette'):
        self.population_size = config_dict['POPULATION_SIZE']
        self.generation_size = config_dict['GENERATION_SIZE']
        self.load_rest_time = config_dict['LOAD_REST_TIME']
        self.elitism_rate = config_dict['ELITISM_RATE']
        self.mutation_rate = config_dict['MUTATION_RATE']
        self.start_time = config_dict['START_TIME']
        self.finish_time = config_dict['FINISH_TIME']
        self.blocks = config_dict['BLOCKS']

        self.transporter_container = self.read_transporters_from_file(transporter_path)
        self.block_container = self.read_blocks_from_file(block_path)
        self.map_path = map_path
        self.selection_method = selection_method

    def create_blocks_from_node(self, map_path):
        if map_path:
            file_manager = FileManager()
            return file_manager.create_block_from_graph_file(map_path, self.blocks)

    def read_transporters_from_file(self, transporter_path):
        file_manager = FileManager()
        return file_manager.load_transporters(transporter_path)

    def read_blocks_from_file(self, block_path):
        file_manager = FileManager()
        return file_manager.load_block_data(block_path)

    def set_GA_config(self, config_dict):
        self.population_size = config_dict['POPULATION_SIZE']
        self.generation_size = config_dict['GENERATION_SIZE']
        self.load_rest_time = config_dict['LOAD_REST_TIME']
        self.elitism_rate = config_dict['ELITISM_RATE']
        self.mutation_rate = config_dict['MUTATION_RATE']
        self.start_time = config_dict['START_TIME']
        self.finish_time = config_dict['FINISH_TIME']
        self.blocks = config_dict['BLOCKS']

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

    config = Configuration(transporter_path, block_path, config_dict)

    transporter_container = file_manager.load_transporters(transporter_path)
    block_container = file_manager.load_block_data(block_path, 100)

    ga = GA(config.transporter_container, config.block_container, config.get_GA_config(), config.selection_method)
    ga.run_GA()
