# 블록 데이터 또는 트랜스포터 데이터를 그래프로 측정하는 파일
import matplotlib.pyplot as plt
import random
import numpy as np

def plot_histogram(data, max_x):
    bins = np.arange(0, max_x+50, 100)
    plt.hist(data, bins=bins, color='skyblue', edgecolor='black', linewidth=1.2)

    plt.xticks(bins)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Data')

    plt.show()

li = []
for i in range(100):
    a = random.choices(range(1, 9), weights=[0.01, 0.06, 0.15, 0.18, 0.19, 0.20, 0.21, 0.01])
    b = random.randint(a[0] * 100 - 100, a[0] * 100)
    li.append(b)

plot_histogram(li, 700)
