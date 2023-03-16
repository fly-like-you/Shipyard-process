import matplotlib.pyplot as plt
from transporter.transporter.GA_schedule.ScheduleGA import ScheduleGA
from transporter.transporter.GA_schedule.Selection import Selection


def plot_multiple_list_data(data_list, dot_list=None, color_list=None):
    if not color_list:
        color_list = ['blue', 'red', 'green']  # 기본값 설정

    x = range(len(data_list[0]))  # x축 범위는 첫 번째 리스트 데이터의 길이로 설정

    for i, data in enumerate(data_list):
        y = data
        color = color_list[i % len(color_list)]  # color_list를 순환하도록 설정

        plt.plot(x, y, color=color)
        plt.scatter(x, y, color=color, s=10)
        if dot_list:
            for j, dot in enumerate(dot_list):
                color = color_list[j % len(color_list)]  # color_list를 순환하도록 설정

                plt.scatter(dot, data_list[i][dot], color=color, s=30)

    plt.show()




ga = ScheduleGA(blocks, population_size=10, max_generation=300)
select_size = 50
data_list = []
dot_list = []
for i in range(1):
    population = ga.init_population()
    block_dict = ga.block_dict_init()
    selection = Selection(population, block_dict)
    cum_prob = selection.selection2()
    # for _ in range(select_size):
    #     parents = selection.get_parent_index()
    #     dot_list.append(parents)
    data_list.append(cum_prob)

colors = ['blue', 'red', 'green']
plot_multiple_list_data(data_list=data_list, color_list=colors)