from matplotlib import pyplot as plt
import numpy as np
from util import weight, maze


def order(df):
    task_list = df['block_number'].tolist()
    # print(task_list)

    task_list_len = len(task_list)

    task_list_set = []
    for num, i in enumerate(task_list):
        if i not in task_list_set:
            task_list_set.append(i)
    task_num = [i for i in range(len(task_list_set))]
    y_axis = []
    for i in task_list:
        if i in task_list_set:
            y_axis.append(task_num[task_list_set.index(i)])
    hline_list = []

    for num, i in enumerate(task_num):
        xminxmax = []
        for num1, j in enumerate(y_axis):
            if i == j:
                xminxmax.append(num1)
        xminxmax.append(num)
        hline_list.append(xminxmax)

    xx = []
    yy = []
    block = []
    for i in hline_list:
        block.append(i[-1])
        if len(i) != 3:
            xx.append(i[0])
            yy.append(task_list_len)
        else:
            xx.append(i[0])
            yy.append(i[1])

    # plt.scatter(xx, yy)
    # plt.axline([0, 0], [task_list_len, task_list_len])
    # print(hline_list)
    #
    # for num, i in enumerate(hline_list):
    #     plt.annotate(i[-1], (xx[num], yy[num]))
    # plt.xlabel('in')
    # plt.ylabel('out')
    # plt.title('order scatter')
    # plt.show()

    # TODO:y값 같을 때 처리 해야함
    # exist_block = []
    block_relation = {}
    for num, i in enumerate(hline_list):
        # if not i[-1] in exist_block:
            y_value = yy[num]
            x_value = xx[num]
            area_1 = []
            area_2 = []
            area_3 = []
            area_4 = []
            area_5 = []
            area_6 = []

            for y_index, y in enumerate(yy):
                if y > y_value:
                    if xx[y_index] > x_value:
                        if xx[y_index] > y_value:
                            area_6.append(y_index)
                        else:
                            area_5.append(y_index)
                    else:
                        area_3.append(y_index)
                elif y < y_value:
                    if xx[y_index] < x_value:
                        if yy[y_index] > x_value:
                            area_2.append(y_index)
                        else:
                            area_1.append(y_index)
                    else:
                        area_4.append(y_index)

            over = area_3 + area_5
            over_list = sorted([yy[i]for i in over])
            over_index = [yy.index(i) for i in over_list]
            under = area_2 + area_4
            under_list = sorted([yy[i] for i in under])
            under_index = [yy.index(i) for i in under_list]
            batch_list = under_index + [num] + over_index
            batch_block = [hline_list[i][-1] for i in batch_list]
            # print(num, batch_block)
            block_relation[i[-1]] = batch_block

            # for exist in batch_block:
            #     exist_block.append(exist)
            # print(batch_block)
    # print(exist_block)
    # print(block_relation)
    # input()
    # return xx, yy, block
    return block_relation


def init_weight(map, weight_map, df, out_block_cnt):

    task_list = df['block_number'].tolist()
    task_list_len = len(task_list)

    task_list_set = []
    for num, i in enumerate(task_list):
        if i not in task_list_set:
            task_list_set.append(i)

    hline_list = []
    for i in task_list_set:
        inout = []
        for vv, j in enumerate(task_list):
            if i == j:
               inout.append(vv)
        if len(inout) == 1:
            inout.append(-1)
        inout.append(i)
        hline_list.append(inout)
    print(hline_list)

    xx = []
    yy = []
    block = []
    for i in hline_list:
        block.append(i[-1])
        if len(i) != 3:
            xx.append(i[0])
            yy.append(task_list_len)
        else:
            xx.append(i[0])
            yy.append(i[1])

    # plt.scatter(xx, yy)
    # plt.axline([0, 0], [task_list_len, task_list_len])
    #
    # for num, i in enumerate(hline_list):
    #     # print(i[-1])
    #     plt.annotate(i[-1], (xx[num], yy[num]))
    # plt.xlabel('in')
    # plt.ylabel('out')
    # plt.title('order scatter')
    # plt.show()

    y = sorted(yy)
    y_order = []
    for i in y:
        for z in hline_list:
            if i == z[1]:
                y_order.append(z[2])

    s = maze.Maze(map.map, map.block_max_size, map.block_max_size)
    start = s.find_start(map.flag)
    pos_loc = []
    for i in start:
        pos_loc.extend(s.bfs(i))
    weight_list = weight.weight_cal(pos_loc, weight_map, map.block_max_size, map.block_max_size)

    min_weight = min(weight_list)
    max_weight = max(weight_list)
    distance = (max_weight-min_weight)/out_block_cnt
    init = []
    for _ in y_order:
        min_weight = min_weight + distance
        init.append(round(min_weight,2))

    map.y_order = y_order
    # map.weight = sorted(init, reverse=True)
    map.weight = init


# 1자로 연결
def order_old(df):
    task_list = df['block_number'].tolist()
    x_axis = [i for i in range(len(task_list))]
    task_list_set = []
    for num, i in enumerate(task_list):
        if i not in task_list_set:
            task_list_set.append(i)

    task_num = [i for i in range(len(task_list_set))]
    y_axis = []
    for i in task_list:
        if i in task_list_set:
            y_axis.append(task_num[task_list_set.index(i)])

    hline_list = []
    for num, i in enumerate(task_num):
        xminxmax = []
        for num1, j in enumerate(y_axis):
            if i == j:
                xminxmax.append(num1)
        xminxmax.append(num)
        hline_list.append(xminxmax)

    # plt.scatter(x_axis, list(map(str, task_list_set)))
    plt.scatter(x_axis, y_axis)

    for i in hline_list:
        if len(i) != 3:
            continue
        plt.hlines(y=i[2], xmin=i[0], xmax=i[1])
    for num, i in enumerate(task_list):
        plt.annotate(i, (x_axis[num], y_axis[num]))
    plt.xlabel('curr')
    plt.ylabel('block')
    plt.title('order scatter')
    plt.show()

    return x_axis, y_axis


def order1(df):
    # print(df)
    # print(df[df.type == 1])  # 입고인 블럭만
    # print(df[df.duplicated(['block_number']) == True])  # 당일 입고 되었다가 출고되는 블럭
    # exist_block = df[df.position_x != 0]
    # print(exist_block)
    # y = list(range(len(exist_block)))
    # x_axis = exist_block.append(df[df.type == 1]).reset_index()  # x 축
    # print(df)
    x_axis = df[df.type == 1].reset_index(drop=True)
    y_axis = df[df.type == 2].reset_index(drop=True)  # y 축

    #
    # print(x_axis)
    # print(y_axis)

    x_axis_list = x_axis['block_number'].tolist()
    # print("x_axis_list ", x_axis_list)
    # print(y)
    y_axis_list = []

    temp_list = []
    dup_list = []
    dup_del_list = []
    dup_set = set()

    # 중복 요소 찾기
    for i, j in enumerate(x_axis_list):
        if j in temp_list:
            dup_set.add(j)
        else:
            temp_list.append(j)
    # 중복 요소의 각 인덱스 찾기
    for i in dup_set:
        indexes = [a for a, b in enumerate(x_axis_list) if i == b]
        dup_list.append(indexes)
    # 맨 뒤 값 제외한 인덱스 만
    dup_del_list = [j for i in dup_list for j in i[:-1]]
    # print(dup_list)
    # print(dup_del_list)
    # 중복 제거
    for index in sorted(dup_del_list, reverse=True):
        del x_axis_list[index]

    x_len = len(x_axis_list)
    for i in range(x_len):
        y = y_axis.loc[x_axis_list[i] == y_axis.block_number, 'block_number'].index.tolist()
        if not y:
            y_axis_list.append(x_len)
        else:
            y_axis_list.extend(y)
        # y_axis.loc[x_axis_list[i] == y_axis.block_number, 'block_number'].index.value


    # # print("x_axis_list", x_axis_list)
    # # print("y_axis_list ", y_axis_list)
    # x_axis_list_str = list(map(str, x_axis_list))
    # y_axis_list_str = list(map(str, y_axis_list))
    # # ######################################
    # print(x_axis_list)
    # print(y_axis_list)
    # plt.plot(x_axis_list_str, y_axis_list, 'ok')
    # # helper = np.arange(len(x_axis_list_str))
    # # helper1 = np.arange(len(y_axis_list_str))
    # # plt.xticks(ticks=helper, labels=x_axis_list_str)
    # # plt.yticks(ticks=helper1, labels=y_axis_list_str)
    # plt.xlabel('in order')
    # plt.ylabel('out order')
    # plt.title('order scatter')
    # plt.show()
    # # plt.close()
    # print(x_axis_list)
    # print(y_axis_list)

    return x_axis_list, y_axis_list
