import random
import numpy as np
import pandas as pd
import math
import copy
from copy import deepcopy
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
    init_weight_order = [init_weight_list[y_order.index(i)] for i in y_order]
    # print(num)
    # print(init_weight_order)
    # print(y_order.index(num), init_weight)
    init_weight_order_small = init_weight_order[:y_order.index(num)]
    init_weight_order_big = init_weight_order[y_order.index(num) + 1:]
    block_list = block_dict[num]
    # pre_weight_list = [init_weight_list[y_order.index(i)] for i in block_list]
    # small = pre_weight_list[:block_list.index(num)]
    # big = pre_weight_list[block_list.index(num) + 1:]
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

    # 들어갈수 잇는 최단거리 리스트에서 초기값에 가장 가까운 최단거리를 찾음
    nearest = findNearNum(weight_list, init_weight)

    # 동기화
    for i, j in enumerate(init_weight_order_small):
        if j >= nearest[1]:
            init_weight_order_small[i] = nearest[1]

    for i, j in enumerate(init_weight_order_big):
        if j <= nearest[1]:
            init_weight_order_big[i] = nearest[1]

    # map1.weight = init_weight_order_small + [init_weight] + init_weight_order_big

    min_range = None
    max_range = None
    for i in sorted(init_weight_order_small, reverse=True):
        if i < nearest[1]:
            min_range = i
            break
    for i in init_weight_order_big:
        if i > nearest[1]:
            max_range = i
            break

    best_insert_loc = []
    if min_range is not None and max_range is not None:
        for i, j in enumerate(weight_list):
            if min_range <= j <= max_range:
                best_insert_loc.append(pos_loc[i])

    elif min_range is not None and max_range is None:
        for i, j in enumerate(weight_list):
            if min_range <= j:
                best_insert_loc.append(pos_loc[i])

    elif min_range is None and max_range is not None:
        for i, j in enumerate(weight_list):
            if max_range >= j:
                best_insert_loc.append(pos_loc[i])

    elif min_range is None and max_range is None:
        for i, j in enumerate(weight_list):
            best_insert_loc.append(pos_loc[i])

    alter_insert_loc = [loc for loc in pos_loc if loc not in best_insert_loc]

    avail_loc = []
    # if avail_loc:
    s = maze.Maze(map1.map, map1.block_max_size, map1.block_max_size)
    start = s.find_start(flag)
    vvlist =[]
    # 1차적으로 근접한 입고 가능 구간 확인
    for j in start:
        for _, i in enumerate(best_insert_loc):
            ok = 1
            before_maze = maze.Maze(map1.map, map1.block_max_size, map1.block_max_size)
            before_maze_path = before_maze.bfs(j)
            before_maze_map = before_maze.maze_map
            print("before")
            print(before_maze_map)
            map1.map[i[0]:i[0] + height, i[1]:i[1] + width] = 1
            print(map1.map)
            after_maze = maze.Maze(map1.map, map1.block_max_size, map1.block_max_size)
            after_maze_path = after_maze.bfs(j)
            after_maze_map = after_maze.maze_map
            print(after_maze_map)
            map1.map[i[0]:i[0] + height, i[1]:i[1] + width] = 0
            if len(after_maze_path) == 0:
                break
            vvvv = 0
            for bb in before_maze_path[:]:
                if after_maze_map[bb[0]][bb[1]] == 0:
                    vvvv += 1
                    before_maze_path.remove(bb)

            for nn in before_maze_path:
                if nn not in after_maze_path:
                    ok = 0
                    break
            # input()
            if ok == 1:
                vvlist.append(vvvv)
                avail_loc.append(i)
                # best_insert_loc.remove(i)
    print(vvlist)
    print(len(vvlist))

    avail_loc = list(set(avail_loc))
    avail_loc_num = []
    # 위의 조건을 만족하지 못할시
    if not avail_loc:
        # print('not')
        for j in start:
            for _, i in enumerate(alter_insert_loc):
                ok = 1
                before_maze = maze.Maze(map1.map, map1.block_max_size, map1.block_max_size)
                before_maze_map_1 = before_maze.maze
                before_maze_map = before_maze.maze_map
                before_maze_path = before_maze.bfs(j)
                map1.map[i[0]:i[0] + height, i[1]:i[1] + width] = 1
                after_maze = maze.Maze(map1.map, map1.block_max_size, map1.block_max_size)
                after_maze_map_1 = after_maze.maze
                after_maze_map = after_maze.maze_map
                after_maze_path = after_maze.bfs(j)
                map1.map[i[0]:i[0] + height, i[1]:i[1] + width] = 0
                # vvvv = 0
                for bb in before_maze_path[:]:
                    if after_maze_map[bb[0]][bb[1]] == 0:
                        # vvvv += 1
                        before_maze_path.remove(bb)

                for nn in before_maze_path:
                    if nn not in after_maze_path:
                        ok = 0
                        break

                # input()
                if ok == 1:
                    avail_loc.append(i)
                    # avail_loc_num.append(vvvv)
                    # alter_insert_loc.remove(i)

        # min(avail_loc_num)
        avail_loc = list(set(avail_loc))
        # print(avail_loc)
        if not avail_loc:  # 들어갈 공간 X
            # print("반입 불가!!")
            count += 1
            area += width * height
            df.loc[df.block_number == num, 'position_x'] = None
            df.loc[df.block_number == num, 'position_y'] = None
            return count, area
        # print('not')
        # print(avail_loc)
        aaaa = weight.weight_cal(avail_loc, weight_map, height, width)
        # print("aaaa", aaaa)
        nearest = findNearNum(aaaa, init_weight)
        # print(nearest)
        avail_loc = [avail_loc[index] for index, zccc in enumerate(aaaa) if nearest[1] == zccc]

    # print("avail", avail_loc)
    avail_loc_num = []
    for i in avail_loc:
        temp = []
        map1.map[i[0]:i[0] + height, i[1]:i[1] + width] = 1
        s = maze.Maze(map1.map, map1.block_max_size, map1.block_max_size)
        start = s.find_start(flag)
        for j in start:
            temp.extend(s.bfs(j))
        avail_loc_num.append(len(temp))
        map1.map[i[0]:i[0] + height, i[1]:i[1] + width] = 0

    # print(avail_loc_num)
    # print(max(avail_loc_num))
    best_position_list = [num for num, i in enumerate(avail_loc_num) if i == max(avail_loc_num)]
    best_position = avail_loc[random.choice(best_position_list)]
    # print(best_position)
    # print(best_position)
    max_weight = weight_list[pos_loc.index(best_position)]
    # print(max_weight)
    # 동기화
    for i, j in enumerate(init_weight_order_small):
        if j >= max_weight:
            init_weight_order_small[i] = max_weight

    for i, j in enumerate(init_weight_order_big):
        if j <= max_weight:
            init_weight_order_big[i] = max_weight
    map1.weight = init_weight_order_small + [max_weight] + init_weight_order_big
    # print(max_weight)
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
