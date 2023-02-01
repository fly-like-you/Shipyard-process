from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np

# 2d box 그리기
def boxplot_2d(x,y, ax, fc, label, whis=1.5):
    xlimits = [np.percentile(x, q) for q in (25, 50, 75)]
    ylimits = [np.percentile(y, q) for q in (25, 50, 75)]

    ##the box
    box = Rectangle(
        (xlimits[0],ylimits[0]),
        (xlimits[2]-xlimits[0]),
        (ylimits[2]-ylimits[0]),
        ec='k',
        fc=fc,
        zorder=0,
        label=label
    )
    ax.add_patch(box)

    ##the x median
    vline = Line2D(
        [xlimits[1],xlimits[1]],[ylimits[0],ylimits[2]],
        color='k',
        zorder=1
    )
    ax.add_line(vline)

    ##the y median
    hline = Line2D(
        [xlimits[0],xlimits[2]],[ylimits[1],ylimits[1]],
        color='k',
        zorder=1
    )
    ax.add_line(hline)

    ##the central point
    ax.plot([xlimits[1]],[ylimits[1]], color='k', marker='o')

    ##the x-whisker
    ##defined as in matplotlib boxplot:
    ##As a float, determines the reach of the whiskers to the beyond the
    ##first and third quartiles. In other words, where IQR is the
    ##interquartile range (Q3-Q1), the upper whisker will extend to
    ##last datum less than Q3 + whis*IQR). Similarly, the lower whisker
    ####will extend to the first datum greater than Q1 - whis*IQR. Beyond
    ##the whiskers, data are considered outliers and are plotted as
    ##individual points. Set this to an unreasonably high value to force
    ##the whiskers to show the min and max values. Alternatively, set this
    ##to an ascending sequence of percentile (e.g., [5, 95]) to set the
    ##whiskers at specific percentiles of the data. Finally, whis can
    ##be the string 'range' to force the whiskers to the min and max of
    ##the data.
    iqr = xlimits[2]-xlimits[0]

    ##left
    try:
        left = np.min(x[x > xlimits[0]-whis*iqr])
    except:
        left = 0
    whisker_line = Line2D(
        [left, xlimits[0]], [ylimits[1],ylimits[1]],
        color='k',
        zorder=1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [left, left], [ylimits[0],ylimits[2]],
        color = 'k',
        zorder = 1
    )
    ax.add_line(whisker_bar)

    ##right
    try:
        right = np.max(x[x < xlimits[2]+whis*iqr])

    except:
        right = 0

    whisker_line = Line2D(
        [right, xlimits[2]], [ylimits[1],ylimits[1]],
        color = 'k',
        zorder = 1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [right, right], [ylimits[0],ylimits[2]],
        color = 'k',
        zorder = 1
    )
    ax.add_line(whisker_bar)

    ##the y-whisker
    iqr = ylimits[2]-ylimits[0]

    ##bottom
    try:
        bottom = np.min(y[y > ylimits[0]-whis*iqr])
    except:
        bottom = 0
    whisker_line = Line2D(
        [xlimits[1],xlimits[1]], [bottom, ylimits[0]],
        color = 'k',
        zorder = 1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [xlimits[0],xlimits[2]], [bottom, bottom],
        color = 'k',
        zorder = 1
    )
    ax.add_line(whisker_bar)

    ##top
    try:
        top = np.max(y[y < ylimits[2]+whis*iqr])
    except:
        top = 0
    whisker_line = Line2D(
        [xlimits[1],xlimits[1]], [top, ylimits[2]],
        color = 'k',
        zorder = 1
    )
    ax.add_line(whisker_line)
    whisker_bar = Line2D(
        [xlimits[0],xlimits[2]], [top, top],
        color = 'k',
        zorder = 1
    )
    ax.add_line(whisker_bar)

    ##outliers
    mask = (x<left)|(x>right)|(y<bottom)|(y>top)
    ax.scatter(
        x[mask],y[mask],
        facecolors='none', edgecolors='k'
    )


def draw_figure(ax, x, y, label, title):
    # colors = np.random.rand(len(x))
    # cmap = plt.cm.RdYlBu_r
    # c = cmap(colors)
    c = ['r', 'g', 'b', 'c']
    # fig = plt.figure()
    # ax = fig.subplots()

    for i in range(len(x)):
        x_array = np.array(x[i])
        y_array = np.array(y[i])
        boxplot_2d(x_array, y_array, ax, c[i], label[i], whis=1.5)

    ax.legend(loc='upper left', frameon=True)
    ax.set_title(str(title))
    ax.set_xlabel('out count')
    ax.set_ylabel('insert area')
    # plt.show()

    # fig = plt.figure(1)
    # ax = fig.add_subplot(111,projection='3d')
    # ax.plot(x_diff_depth, y_diff_depth, z_diff_depth, 'o', label='depth')
    # ax.plot(x_diff_2quad, y_diff_2quad, z_diff_2quad, 's', label='2quad')
    # ax.plot(x_diff_4quad, y_diff_4quad, z_diff_4quad, 'd', label='4quad')
    # ax.legend(loc='upper left', frameon=True)
    # ax.set_xlabel('area')
    # ax.set_ylabel('insert count')
    # ax.set_zlabel('out count')
    # plt.show()
    # plt.close()

    # markers = ['o', 's', 'd']
    # plt.plot(x_diff_depth, y_diff_depth, 'o', label='depth')
    # plt.plot(x_diff_2quad, y_diff_2quad, 's', label='2quad')
    # plt.plot(x_diff_4quad, y_diff_4quad, 'd', label='4quad')
    # plt.axvline(x=0, color='r', linewidth=1)
    # plt.axhline(y=0, color='r', linewidth=1)
    # plt.legend(loc='upper left', frameon=True)
    # plt.rc('font', family='Malgun Gothic')
    # plt.xlabel('area')
    # plt.ylabel('count')
    # plt.show()
    # plt.close()


def scatter(ax, x, y, label, flg, param):

    for i, j in enumerate(x):
        x[i] = np.mean(j)
    for i, j in enumerate(y):
        y[i] = np.mean(j)

    marker = ['o', 's', 'd', '*', 'x', '^']

    for i, _ in enumerate(x):
        ax.plot(x[i], y[i], marker[i], label=label[i])

    # plt.axvline(x=0, color='r', linewidth=1)
    # plt.axhline(y=0, color='r', linewidth=1)
    ax.legend(loc='upper right', frameon=True)
    # ax.rc('font', family='Malgun Gothic')
    ax.set_title('{}{}'.format(flg, param))
    ax.set_xlabel('count')
    ax.set_ylabel('area')