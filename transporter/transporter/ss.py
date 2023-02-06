import time
import sys
import matplotlib.pyplot as plt
import numpy as np




def plot_moving_average(data, window_size, color, label):
    moving_average = np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    plt.plot(moving_average, linestyle='--', color=color, label=label)
    plt.legend(loc='best')

def measure_time(function, *args, **kwargs):
    start_time = time.time()
    result, performance = function(*args, **kwargs)
    return time.time() - start_time, result, performance

try:
    exec(open("GA.py", encoding='UTF8').read(), globals())
    exec(open("GA_notGA.py", encoding='UTF8').read(), globals())
except Exception as e:
    sys.stderr.write("Error: " + str(e))
    sys.exit(1)

times1 = []
performance_li1 = []
times2 = []
performance_li2 = []

GRAPH_COUNT = 20
for i in range(GRAPH_COUNT):
    print(i)
    execution_time, result, performance = measure_time(run_ga)
    execution_time2, result2, performance2 = measure_time(run_ga2)

    performance_li1.append(performance)
    times1.append(execution_time)
    performance_li2.append(performance2)
    times2.append(execution_time2)


plt.plot([t for t in range(GRAPH_COUNT)],performance_li1, color='#e35f62', label='onlyGA')
plt.legend(loc='best')

plot_moving_average(performance_li1, 5, '#e35f62', 'onlyGA')

plt.plot([t for t in range(GRAPH_COUNT)],performance_li2, color='green', label='notGA')
plot_moving_average(performance_li2, 5, 'green', 'notGA')
plt.legend(loc='best')

plt.ylabel('algorithm performance enhence percent')
plt.xlabel('file execution time')
plt.title('Execution time of function over 30 runs')
plt.ylim([60,100])
plt.show()
