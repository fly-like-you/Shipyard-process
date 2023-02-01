import random
import numpy as np
import pandas as pd
import math
import copy
from util import weight, check_maze, maze, order


def insert(block, map1, weight_map, count, area, df, flag):
    block_dict = order.order(df)
    minsize = 50
    maxsize = 255
    ran_num = random.randint(minsize, maxsize)  # 블록 색깔
    # print("반입 함수")
    num = block.block_number  # 블록 번호
    pre_weight = 0
    # print('해당 블록 num', num)
    y_order = map1.y_order
    init_weight_list = map1.weight
    init_weight = init_weight_list[y_order.index(num)]
    asdfsadf = [init_weight_list[y_order.index(i)] for i in y_order]
    print(asdfsadf)
    print(y_order.index(num), init_weight)
    asdfsadf_small = asdfsadf[:y_order.index(num)]
    asdfsadf_big = asdfsadf[y_order.index(num) + 1:]
    block_list = block_dict[num]
    pre_weight_list = [init_weight_list[y_order.index(i)] for i in block_list]
    small = pre_weight_list[:block_list.index(num)]
    big = pre_weight_list[block_list.index(num) + 1:]
    # print(pre_weight_list)
    # print(small)
    # print(big)

    pos_loc = []  # 가능 위치
    width = block.width  # 가로 길이
    height = block.height  # 세로 길이
    s = maze.Maze(map1.map, width, height)
    start = s.find_start(flag)  # 들어갈수 있는 입구
    # print(start)
    # print(sorted(start))

    if len(start) == 0:  # 들어갈 공간 X
        # print("반입 불가!!")
        count += 1
        area += width * height
        df.loc[df.block_number == num, 'position_x'] = None
        df.loc[df.block_number == num, 'position_y'] = None
        return count, area

    for i in start:
        pos_loc.extend(s.bfs(i))

    if len(pos_loc) == 0:  # 입구 밖에 안될 때
        pos_loc.extend(start)

    weight_list = weight.weight_cal(pos_loc, weight_map, height, width)

    nearest = findNearNum(weight_list, init_weight)

    for i, j in enumerate(asdfsadf_small):
        if j >= nearest[1]:
            asdfsadf_small[i] = nearest[1]

    for i, j in enumerate(asdfsadf_big):
        if j <= nearest[1]:
            asdfsadf_big[i] = nearest[1]

    map1.weight = asdfsadf_small+ [init_weight] + asdfsadf_big

    min_range = None
    max_range = None
    for i in sorted(asdfsadf_small, reverse=True):
        if i < nearest[1]:
            min_range = i
            break
    for i in asdfsadf_big:
        if i > nearest[1]:
            max_range = i
            break

    insert_loc = []
    if min_range is not None and max_range is not None:
        for i, j in enumerate(weight_list):
            if min_range <= j <= max_range:
                insert_loc.append(pos_loc[i])

    elif min_range is not None and max_range is None:
        for i, j in enumerate(weight_list):
            if min_range <= j:
                insert_loc.append(pos_loc[i])

    elif min_range is None and max_range is not None:
        for i, j in enumerate(weight_list):
            if max_range >= j:
                insert_loc.append(pos_loc[i])

    elif min_range is None and max_range is None:
        for i, j in enumerate(weight_list):
            insert_loc.append(pos_loc[i])


    avail_loc_num = []
    for _, i in enumerate(insert_loc):
        avail_loc = []
        map1.map[i[0]:i[0] + height, i[1]:i[1] + width] = 1
        # map1.map_color[i[0]:i[0] + height, i[1]:i[1] + width] = ran_num
        s = maze.Maze(map1.map, map1.block_max_size, map1.block_max_size)
        start = s.find_start(flag)  # 들어갈수 있는 입구
        for j in start:
            avail_loc.extend(s.bfs(j))
        avail_loc_num.append(len(avail_loc))
        map1.map[i[0]:i[0] + height, i[1]:i[1] + width] = 0
        # map1.map_color[i[0]:i[0] + height, i[1]:i[1] + width] = 0
    print(max(avail_loc_num))
    best_position_list = [num for num, i in enumerate(avail_loc_num) if i == max(avail_loc_num)]
    best_position = insert_loc[random.choice(best_position_list)]
    print(best_position)
    max_weight = weight_list[pos_loc.index(best_position)]
    print(max_weight)
    df.loc[df.block_number == num, 'position_x'] = best_position[1]
    df.loc[df.block_number == num, 'position_y'] = best_position[0]
    df.loc[df.block_number == num, 'weight_val'] = max_weight

    map1.map[best_position[0]:best_position[0] + height, best_position[1]:best_position[1] + width] = 1
    map1.map_color[best_position[0]:best_position[0] + height, best_position[1]:best_position[1] + width] = ran_num

    block_data = block.to_dict()  # 블록 데이터 가공
    block_data['position_x'] = best_position[1]
    block_data['position_y'] = best_position[0]
    block_data['weight_val'] = max_weight

    map1.block_data(block_data)  # 맵 객체에 블록 데이터 추가

    return count, area


def findNearNum(exList, values):
    answer = [0 for _ in range(2)]  # answer 리스트 0으로 초기화

    minValue = min(exList, key=lambda x: abs(x - values))
    minIndex = exList.index(minValue)
    answer[0] = minIndex
    answer[1] = minValue

    return answer
