import random
import pandas as pd
import math
import copy
from util import weight, check_maze, maze, order


def insert(block, map1, weight_map, count, area, df, flag, exist_block_num):
    minsize = 50
    maxsize = 255
    ran_num = random.randint(minsize, maxsize)  # 블록 색깔
    # print("반입 함수")
    num = block.block_number  # 블록 번호

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

    # print(weight_list)

    insert_loc = pos_loc[weight_list.index(max(weight_list))]  # 가중치 합이 제일 높은 곳에 반입

    # print(insert_loc)

    # insert_loc = random.choice(pos_loc)

    # print("적제 가능 위치 y,x = ", pos_loc)
    # print("적치 위치 y,x = ", insert_loc)

    df.loc[df.block_number == block.block_number, 'position_x'] = insert_loc[1]
    df.loc[df.block_number == block.block_number, 'position_y'] = insert_loc[0]
    df.loc[df.block_number == block.block_number, 'weight_val'] = max(weight_list)

    map1.map[insert_loc[0]:insert_loc[0]+height, insert_loc[1]:insert_loc[1]+width] = 1
    map1.map_color[insert_loc[0]:insert_loc[0] + height, insert_loc[1]:insert_loc[1] + width] = ran_num

    block_data = block.to_dict()  # 블록 데이터 가공
    block_data['position_x'] = insert_loc[1]
    block_data['position_y'] = insert_loc[0]
    block_data['weight_val'] = max(weight_list)

    map1.block_data(block_data)  # 맵 객체에 블록 데이터 추가

    return count, area
