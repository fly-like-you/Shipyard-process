import random
import pandas as pd
import math
import copy
from util import weight, check_maze, maze, order


def insert(block, map1, weight_map, count, area, df, flag, exist_block_num):
    x_axis, y_axis = order.order(df)
    minsize = 50
    maxsize = 255
    ran_num = random.randint(minsize, maxsize)  # 블록 색깔
    # print("반입 함수")
    num = block.block_number  # 블록 번호
    pre_weight = 0
    # print('해당 블록 num', num)
    x_index = x_axis.index(num)  # x 축 인덱스 번호
    y_index = y_axis[x_index]  # y 축 값
    # print(x_index, y_index)
    consider_list = y_axis[:x_index]  # 고려해야하는 y축 리스트
    # print("consider", consider_list)
    y_axis_list = [y for y in consider_list if y_index < y]  # 나보다 늦게 출고가 되는 y축 리스트
    print("y축", y_axis_list)
    x_axis_block_index = [p for p, q in enumerate(consider_list) if q in y_axis_list]  # weight list 해당되는 x 축 인덱스
    x_axis_block_num = [x_axis[i] for i in x_axis_block_index]  # x축 인덱스에 해당하는 x 축 블록 번호
    # print("나중에 출고되는 블록", x_axis_block_num)
    # print("weight_list", weight_list)
    # print(x_axis_block_index, x_axis_block_num)
    pre_weight_list = [df[df.block_number == i]['weight_val'].values[0] for i in x_axis_block_num]  # 해당 블록 weight_val 값
    if pre_weight_list:  # 2사분면에 있다면 초이스
        pre_weight = min(pre_weight_list)

    pos_loc = []  # 가능 위치
    width = block.width  # 가로 길이
    height = block.height  # 세로 길이
    s = maze.Maze(map1.map, width, height)
    start = s.find_start(flag)  # 들어갈수 있는 입구
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
        # print(s.maze_map)
        # print("입구밖에 안돼!!", pos_loc)

    weight_list = weight.weight_cal(pos_loc, weight_map, height, width)

    if pre_weight:  # 고려해야하는 가중치 값 존재하면
        weight_list = [i for i in weight_list if i < pre_weight]  # pre_weight 보다 낮은 값들만 사용하는 리스트
    else:   # 2사분면에 아무것도 없다면
        weight_list = []

    # print(num)

    if weight_list:
        # print("YES")
        max_weight = max(weight_list)
        insert_loc = pos_loc[weight_list.index(max_weight)]  # 가중치 합이 제일 높은 곳에 반입
    else:  # weight list 가 없을 때
        # print("no")
        # insert_loc = random.choice(pos_loc)
        # insert_loc = min(pos_loc)
        insert_loc = max(pos_loc)
        max_weight = weight_map[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width].mean()

    df.loc[df.block_number == num, 'position_x'] = insert_loc[1]
    df.loc[df.block_number == num, 'position_y'] = insert_loc[0]
    df.loc[df.block_number == num, 'weight_val'] = max_weight

    map1.map[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width] = 1
    map1.map_color[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width] = ran_num

    block_data = block.to_dict()  # 블록 데이터 가공
    block_data['position_x'] = insert_loc[1]
    block_data['position_y'] = insert_loc[0]
    block_data['weight_val'] = max_weight

    map1.block_data(block_data)  # 맵 객체에 블록 데이터 추가

    return count, area