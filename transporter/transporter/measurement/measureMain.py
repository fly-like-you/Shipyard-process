from transporter.transporter.Configuration import Configuration
from transporter.transporter.measurement.DrawingFunctionPerformance import DrawingFunctionPerformance
from transporter.transporter.GA_refactoring import GA
from transporter.transporter.GA_legacy import run_ga
import os

transporter_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'transporter.csv')
block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'blocks.csv')
config = Configuration(transporter_path, block_path,)

transporter_container = config.transporter_container
block_container = config.block_container
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
ga = GA(transporter_container, block_container, config_dict)

dfp = DrawingFunctionPerformance(
    ga.run_GA,
    run_ga,
    (),
    (transporter_container, block_container),
    10
)

dfp.draw_performance_graph()
dfp.draw_time_graph()
dfp.show()
