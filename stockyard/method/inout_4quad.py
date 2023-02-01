import random
import pandas as pd
import copy
import math
from util import weight, check_maze, maze, order
from method.out_block import out


def insert(block, map1, weight_map, count, area, df, flag, i, exist_block_num, branch):
    # print("반입 함수")
    x_axis, y_axis = order.order(df)
    minsize = 50
    maxsize = 255
    ran_num = random.randint(minsize, maxsize)  # 블록 색깔
    df = df
    step = i
    num = block.block_number  # 블록 번호
    pre_weight = 0
    min_weight = 0
    continue_block = None
    # print('해당 블록 num', num)
    # print("x_axis", x_axis)
    x_index = x_axis.index(num)  # x 축 인덱스 번호
    y_index = y_axis[x_index]  # y 축 값
    x_axis_next = x_axis[x_index + 1:]
    # print("해당 블록", num, " 출고 순서", y_index)
    consider_list_2 = y_axis[:x_index]  # 고려해야하는 y축 리스트
    consider_list_4 = y_axis[x_index + 1:]  # 고려해야하는 Y축 리스트
    # print(consider_list_2)
    # print(consider_list_4)
    y_axis_list_2 = [y for y in consider_list_2 if y_index < y]  # 나보다 늦게 출고가 되는 y축 리스트
    y_axis_list_4 = [y for y in consider_list_4 if y_index > y]  # 나보다 늦게 출고가 되는 y축 리스트
    # print(num)
    # print("왼쪽위", y_axis_list_2)
    # print("오른쪽 밑", y_axis_list_4)
    x_axis_block_index_2 = [p for p, q in enumerate(consider_list_2) if q in y_axis_list_2]  # weight list 해당되는 x 축 인덱스
    x_axis_block_index_4 = [p for p, q in enumerate(consider_list_4) if q in y_axis_list_4]  # weight list 해당되는 x 축 인덱스
    # asdf = [y_axis.index(i) for i in y_axis_list_4]
    # asdf = [x_axis[i] for i in asdf]
    x_axis_block_num_2 = [x_axis[i] for i in x_axis_block_index_2]  # x축 인덱스에 해당하는 x 축 블록 번호
    x_axis_block_num_4 = [x_axis_next[i] for i in x_axis_block_index_4]  # x축 인덱스에 해당하는 x 축 블록 번호
    # print("나중에 출고되는 블록", x_axis_block_num_2)
    # print("전에 출고되는 블록", x_axis_block_num_4)

    if x_axis_block_num_4:  # 4사분면 마지막 블록번호
        continue_block = max(y_axis_list_4)
        continue_block = y_axis.index(continue_block)
        continue_block = x_axis[continue_block]
        # print(continue_block)

    pre_weight_list = [df[df.block_number == i]['weight_val'].values[0] for i in
                       x_axis_block_num_2]  # 해당 블록 weight_val 값

    if pre_weight_list:
        pre_weight = min(pre_weight_list)

    block_list_4 = [[df[df.block_number == i]['width'], df[df.block_number == i]['height']] for i in x_axis_block_num_4]

    pos_loc = []  # 가능 위치
    width = block.width  # 가로 길이
    height = block.height  # 세로 길이

    s = maze.Maze(map1.map, width, height)
    start = s.find_start(flag)  # 들어갈수 있는 입구
    # print("들어갈수있는 입구", start)
    # print(sorted(start))

    if len(start) == 0:  # 들어갈 공간 X
        # print("반입 불가!!")
        if branch == 0:
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
        weight_list = [i for i in weight_list if i <= pre_weight]  # pre_weight 보다 낮은 값들만 사용하는 리스트
    else:
        weight_list = []
    # print("고려 가중치", pre_weight)
    # print("가중치 리스트", weight_list)

    if weight_list:  # 2사분면 고려
        max_weight = max(weight_list)
        insert_loc = pos_loc[weight_list.index(max_weight)]  # 가중치 합이 제일 높은 곳에 반입
        # choice_list = [i for i, value in enumerate(weight_list) if value == max_weight]
        # choice = random.choice(choice_list)
        # insert_loc = pos_loc[choice] # 랜덤 반입
    else:  # weight list 가 없을 때
        insert_loc = random.choice(pos_loc)
        max_weight = weight_map[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width].mean()
    ############################
    ############################
    # print(insert_loc)

    # insert_loc = random.choice(pos_loc)

    # print("적제 가능 위치 y,x = ", pos_loc)
    # print("적치 위치 y,x = ", insert_loc)

    df.loc[df.block_number == num, 'position_x'] = insert_loc[1]
    df.loc[df.block_number == num, 'position_y'] = insert_loc[0]
    df.loc[df.block_number == num, 'weight_val'] = max_weight

    map1.map[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width] = 1
    map1.map_color[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width] = ran_num

    if continue_block is not None and branch == 0:
        temp_x = insert_loc[1]
        temp_y = insert_loc[0]
        branch = 1
        exit_point = continue_block
        # print("자 드가자~!", exit_point)
        copy_df = copy.deepcopy(df)
        map2 = copy.deepcopy(map1)

        curr = step + 1
        quad_4_block_num = []
        while True:
            task = copy_df.loc[curr]
            quad_4_block_num.append(task.block_number)
            if task.type == 1:
                _ = insert(task, map2, weight_map, 0, 0, copy_df, flag, curr, branch)
            if task.type == 2:
                _, copy_df = out(task, map2, 0, flag, copy_df, curr)
            curr += 1
            if task.block_number == exit_point:
                break
            #################################################################
            # 미리한번 돌림
        # min_weight = copy_df[copy_df.block_number == exit_point]['weight_val'].values[0] # 이건 마지막 거리 이용
        min_weight_list = [copy_df[copy_df.block_number == i]['weight_val'].values[0] for i in quad_4_block_num]
        min_weight = max(min_weight_list)  # 4사분면 블록중 가장 높은 최단거리 (이보다 안에 있어야함)
        # print(quad_4_block_num)
        # print(min_weight_list)
        # print(min_weight)

        # print(min_weight)
        # print(pre_weight)
        # print(weight_list)
        map1.map[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width] = 0
        map1.map_color[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width] = 0

        if min_weight:
            weight_list = [i for i in weight_list if min_weight <= i if max_weight >= i]
            # print(weight_list)
            # print("change", weight_list)
            if weight_list:  # 4사분면
                max_weight = max(weight_list)
                insert_loc = pos_loc[weight_list.index(max_weight)]  # 가중치 합이 제일 높은 곳에 반입
                # choice_list = [i for i, value in enumerate(weight_list) if value == max_weight]
                # choice = random.choice(choice_list)
                # insert_loc = pos_loc[choice] # 랜덤 반입
            else:  # weight list 가 없을 때
                # insert_loc = random.choice(pos_loc)
                insert_loc = random.choice(pos_loc)
                min_weight = weight_map[insert_loc[0]:insert_loc[0] + height,
                             insert_loc[1]:insert_loc[1] + width].mean()

        df.loc[df.block_number == num, 'position_x'] = insert_loc[1]
        df.loc[df.block_number == num, 'position_y'] = insert_loc[0]
        df.loc[df.block_number == num, 'weight_val'] = min_weight

        map1.map[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width] = 1
        map1.map_color[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width] = ran_num

    block_data = block.to_dict()  # 블록 데이터 가공
    block_data['position_x'] = insert_loc[1]
    block_data['position_y'] = insert_loc[0]
    block_data['weight_val'] = max_weight

    map1.block_data(block_data)  # 맵 객체에 블록 데이터 추가
    # print(map1.data)
    # print(len(map1.data))
    return count, area


