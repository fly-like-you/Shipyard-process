from transporter.transporter.GA_refactoring.GA_refactoring import GA
from transporter.transporter.Configuration import Configuration, transporter_path, block_path
import random
config_dict = {
    'POPULATION_SIZE': 100,  # 한 세대에서의 인구 수를 설정합니다.
    'GENERATION_SIZE': 1000,  # 몇 세대에 걸쳐 진화할 지 설정합니다.
    'LOAD_REST_TIME': 0.5,  # 트랜스포터가 목적지에서 물건을 실어나르는 시간을 설정합니다 (시)
    'ELITISM_RATE': 0.3,  # 엘리트 individual의 비율을 결정합니다.
    'MUTATION_RATE': 0.3,  # 돌연변이가 일어날 확률을 설정합니다.
    'START_TIME': 9,  # 일과의 시작시간을 결정합니다.
    'FINISH_TIME': 18,  # 일과가 끝나는 시간을 결정합니다.
    'BLOCKS': 100,  # 총 블록 수를 설정합니다. 최대 100개까지 설정가능합니다.
}
def Main():
    pass

    # config = Configuration(transporter_path, block_path, config_dict, selection_method='tournament')
    #
    # ga = GA(config.transporter_container, config.block_container, config.get_GA_config(), config.selection_method)
    # return ga.run_GA()


Main()

