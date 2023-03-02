from transporter.transporter.measurement.DrawingFunctionPerformance import DrawingFunctionPerformance
from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.Configuration import Configuration
from transporter.transporter.GA_refactoring.GA_refactoring import GA
from transporter.transporter.GA_legacy.GA_legacy import run_ga
import os
import matplotlib.pyplot as plt

transporter_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'transporter.csv')
random_block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'blocks.csv')
heavy_block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'heavyBlocks.csv')
light_block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'lightBlocks.csv')


file_manager = FileManager()

light_block_container = file_manager.load_block_data(light_block_path)
heavy_block_container = file_manager.load_block_data(heavy_block_path)
random_block_container = file_manager.load_block_data(random_block_path)

transporter_container = file_manager.load_transporters(transporter_path)

config_dict = {
    'POPULATION_SIZE': 100,  # 한 세대에서의 인구 수를 설정합니다.
    'GENERATION_SIZE': 10,  # 몇 세대에 걸쳐 진화할 지 설정합니다.
    'LOAD_REST_TIME': 0.1,  # 트랜스포터가 목적지에서 물건을 실어나르는 시간을 설정합니다 (시)
    'ELITISM_RATE': 0.4,  # 엘리트 individual의 비율을 결정합니다.
    'MUTATION_RATE': 0.3,  # 돌연변이가 일어날 확률을 설정합니다.
    'START_TIME': 9,  # 일과의 시작시간을 결정합니다.
    'FINISH_TIME': 18,  # 일과가 끝나는 시간을 결정합니다.
    'BLOCKS': 100,  # 총 블록 수를 설정합니다. 최대 100개까지 설정가능합니다.
}

'''
    진화가 진행되면서 우수한 개체를 뽑기 때문에 중복되는 개체가 생기게 되는데
    중복되는 개체에 대해서 시각적인 그래프로 출력하는 파일
'''


def compareToLegacy():
    ga = GA(transporter_container, random_block_container, config_dict)

    dfp = DrawingFunctionPerformance(
        ga.run_GA,
        run_ga,
        (),
        (transporter_container, random_block_container),
        5
    )

    dfp.draw_performance_graph()
    dfp.draw_time_graph()
    dfp.show()


def plot_graphs(x, y_list, labels, title):
    for y, label in zip(y_list, labels):
        plt.plot(x[:len(y)], y, label=label)

    plt.title(title)
    plt.legend()
    plt.show()

def a(block_container, container_title):
    roulette_result = GA(transporter_container, block_container, config_dict, selection_method='roulette').run_GA()
    # sqrt_roulette_result = GA(transporter_container, block_container, config_dict, selection_method='sqrt_roulette').run_GA()
    # square_roulette_result = GA(transporter_container, block_container, config_dict, selection_method='square_roulette').run_GA()
    # tournament_result = GA(transporter_container, block_container, config_dict, selection_method='tournament').run_GA()
    scaled_result = GA(transporter_container, block_container, config_dict, selection_method='scaled_roulette').run_GA()

    result_dict = {
        'roulette_result': roulette_result,
        # 'sqrt_roulette_result': sqrt_roulette_result,
        # 'square_roulette_result': square_roulette_result,
        # 'tournament_result': tournament_result,
        'scaled_roulette': scaled_result
    }

    # keys = list(set(roulette_result.keys()) & set(sqrt_roulette_result.keys()))
    keys = list(set(scaled_result.keys()))
    result_key = list(result_dict.keys())

    result_values = [result_dict[k] for k in result_dict]
    for result in result_values:
        del result['best_individual']

    for key in keys:
        if key == 'best_individual':
            continue
        values = [result[key] for result in result_values]

        plot_graphs(range(len(scaled_result[key])), values, result_key, container_title + " " + key)




if __name__ == '__main__':

    a(random_block_container, 'Random Blocks')

