# 블록 데이터 또는 트랜스포터 데이터를 그래프로 측정하는 파일
import matplotlib.pyplot as plt
import random
import numpy as np
import os
# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc

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

def roulette_selection(population, fitness_values):

    total_fitness = sum(fitness_values)

    # Adjust probabilities based on scale factor
    scale_factor = 1.7
    low_prob = 0.3
    num_low = int(len(population) * 0.4)
    probabilities = [f / total_fitness for f in fitness_values]
    probabilities[:num_low] = [p * low_prob for p in probabilities[:num_low]]
    probabilities[num_low:] = [p * scale_factor for p in probabilities[num_low:]]

    # Calculate cumulative probabilities
    cumulative_prob = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
    plot_cumulative_prob(cumulative_prob)

    # Normalize cumulative probabilities so that the last value is 1
    cumulative_prob = [0] + [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
    normalization_factor = cumulative_prob[-1]
    cumulative_prob = [p / normalization_factor for p in cumulative_prob]

    plot_cumulative_prob(cumulative_prob)


def plot_cumulative_prob(probabilities):
    sqrt_cumulative_prob = np.sqrt(probabilities)

    plt.plot(sqrt_cumulative_prob)
    plt.xlabel('Individual Index')
    plt.ylabel('Cumulative Probability (Square Root)')
    plt.title("하위 40% 확률 0.3배 나머지 1.7배")
    plt.show()


def plot_cumulative_probabilities(population, fitness_values):

    total_fitness = sum(fitness_values)
    probabilities = [f / total_fitness for f in fitness_values]
    cumulative_prob = np.cumsum(probabilities)

    plot_cumulative_prob(cumulative_prob)


def roulette_wheel_selection(population, fitness_values):
    # 적합도 함수를 이용해 적합도 값을 계산합니다
    total_fitness = sum(fitness_values)
    probabilities = [fitness_value / total_fitness for fitness_value in fitness_values]

    # 누적확률 계산
    cumulative_probabilities = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]

    # 누적확률에 대한 라인 그래프 출력
    plt.plot(cumulative_probabilities)
    plt.xlabel('Individual index')
    plt.ylabel('Cumulative probability')
    plt.show()



population = []
fitness_values = []

for i in range(10000):
    population.append(random.randint(0, 9))
    fitness_values.append(random.randint(1, 100))



# 룰렛 휠 함수 호출
roulette_selection(population, fitness_values)






