# 블록 데이터 또는 트랜스포터 데이터를 그래프로 측정하는 파일
import matplotlib.pyplot as plt
import random
import numpy as np
import os
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc

# 윈도우
font_path = r'C:\Windows\Fonts\gulim.ttc'

font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

def plot_histogram(data, max_x):
    # 랜덤하게 생성된 블록의 빈도 수를 출력하기 위해 만든 함수
    # max_x -> 블록의 최대 무게
    bins = np.arange(0, max_x + 50, 100)
    plt.hist(data, bins=bins, color='skyblue', edgecolor='black', linewidth=1.2)

    plt.xticks(bins)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Data')

    plt.show()


def plot_cumulative_prob(probabilities, explain="title"):

    plt.plot(probabilities)
    plt.xlabel('Individual Index')
    plt.ylabel('Cumulative Probability')
    plt.title(explain)
    plt.show()


def scaled_roulette_selection(population, fitness_values):

    total_fitness = sum(fitness_values)

    # 확률에 곱해주기
    scale_factor = 1.7
    low_prob = 0.3
    num_low = int(len(population) * 0.4)
    probabilities = [f / total_fitness for f in fitness_values]
    probabilities[:num_low] = [p * low_prob for p in probabilities[:num_low]]
    probabilities[num_low:] = [p * scale_factor for p in probabilities[num_low:]]

    # 1로 정규화하기
    cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
    normalization_factor = cumulative_prob[-1]
    cumulative_prob = [p / normalization_factor for p in cumulative_prob]

    plot_cumulative_prob(cumulative_prob, "하위 40% 확률 0.3배 나머지 1.7배")

def sqrt_roulette_selection(population, fitness_values):
    total_fitness = sum(fitness_values)

    probabilities = [f / total_fitness for f in fitness_values]

    cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
    sqrt_cumulative_prob = np.sqrt(cumulative_prob)
    plot_cumulative_prob(sqrt_cumulative_prob, "확률 분포 값의 제곱근 씌우기")


def square_roulette_selection(population, fitness_values):
    total_fitness = sum(fitness_values)

    probabilities = [f / total_fitness for f in fitness_values]

    cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
    sqrt_cumulative_prob = np.square(cumulative_prob)
    print(cumulative_prob[50], sqrt_cumulative_prob[50])
    print(cumulative_prob[-1], sqrt_cumulative_prob[-1])


    plot_cumulative_prob(sqrt_cumulative_prob, "확률 분포 값의 제곱")



def plot_cumulative_probabilities(population, fitness_values):

    total_fitness = sum(fitness_values)
    probabilities = [f / total_fitness for f in fitness_values]
    cumulative_prob = np.cumsum(probabilities)

    plot_cumulative_prob(cumulative_prob)



population = []
fitness_values = []

for i in range(10000):
    population.append(random.randint(0, 9))
    fitness_values.append(random.randint(1, 100))



# 룰렛 휠 함수 호출
sqrt_roulette_selection(population, fitness_values)
square_roulette_selection(population, fitness_values)
scaled_roulette_selection(population, fitness_values)





