from transporter.transporter.Configuration import Configuration
from transporter.transporter.measurement.DrawingFunctionPerformance import DrawingFunctionPerformance
from transporter.transporter.GA_refactoring.GA_refactoring import GA
from transporter.transporter.GA_legacy.GA_legacy import run_ga
import os
import matplotlib.pyplot as plt

transporter_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'transporter.csv')
block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'blocks.csv')
config = Configuration(transporter_path, block_path, )

transporter_container = config.transporter_container
block_container = config.block_container
config_dict = {
    'POPULATION_SIZE': 100,  # 한 세대에서의 인구 수를 설정합니다.
    'GENERATION_SIZE': 200,  # 몇 세대에 걸쳐 진화할 지 설정합니다.
    'LOAD_REST_TIME': 0.2,  # 트랜스포터가 목적지에서 물건을 실어나르는 시간을 설정합니다 (시)
    'ELITISM_RATE': 0.3,  # 엘리트 individual의 비율을 결정합니다.
    'MUTATION_RATE': 0.3,  # 돌연변이가 일어날 확률을 설정합니다.
    'START_TIME': 9,  # 일과의 시작시간을 결정합니다.
    'FINISH_TIME': 18,  # 일과가 끝나는 시간을 결정합니다.
    'BLOCKS': 100,  # 총 블록 수를 설정합니다. 최대 100개까지 설정가능합니다.
}


def plot_graph(y_values1, y_values2, y1='', y2='', title=""):
    x_values = list(range(len(y_values2)))
    plt.plot(x_values, y_values1, label=y1)
    plt.plot(x_values, y_values2, label=y2)

    plt.title(title)
    plt.legend()
    plt.show()


def compareToLegacy():
    ga = GA(transporter_container, block_container, config_dict)

    dfp = DrawingFunctionPerformance(
        ga.run_GA,
        run_ga,
        (),
        (transporter_container, block_container),
        5
    )

    dfp.draw_performance_graph()
    dfp.draw_time_graph()
    dfp.show()


roulette_ga = GA(transporter_container, block_container, config_dict, selection_method='roulette')
tournament_ga = GA(transporter_container, block_container, config_dict, selection_method='tournament')
roulette_result = roulette_ga.run_GA()
tournament_result = tournament_ga.run_GA()



def roulette_VS_tournament():
    global roulette_result, tournament_result

    roulette = roulette_result
    tournament = tournament_result

    roulette_work = roulette['work_tp_count']
    tournament_work = tournament['work_tp_count']
    plot_graph(roulette_work, tournament_work, "roulette_tp", "tournament_tp", "roulette vs tournament")


def roulette_VS_tournament_overlap():
    global roulette_result, tournament_result

    roulette = roulette_result
    tournament = tournament_result

    roulette_overlap = roulette['overlap_fit_val_len']
    tournament_overlap = tournament['overlap_fit_val_len']
    plot_graph(roulette_overlap, tournament_overlap, "roulette_fittable_gen", "tournament_fittable_gen",
               "roulette vs tournament (Overlap_len)")


if __name__ == '__main__':
    roulette_VS_tournament()
    roulette_VS_tournament_overlap()
