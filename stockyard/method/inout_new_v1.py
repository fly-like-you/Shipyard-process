import random
import pandas as pd
import math
import copy
from util import weight, check_maze, maze, order

######### 초기 값 적용x  ######

def insert(block, map1, weight_map, count, area, df, flag):
    block_dict = order.order(df)
    minsize = 50
    maxsize = 255
    ran_num = random.randint(minsize, maxsize)  # 블록 색깔
    # print("반입 함수")
    num = block.block_number  # 블록 번호
    pre_weight = 0
    # print('해당 블록 num', num)
    block_list = block_dict[num]
    pre_weight_list = [df[df.block_number == i]['weight_val'].values[0] for i in block_list]
    small = pre_weight_list[:block_list.index(num)]
    big = pre_weight_list[block_list.index(num) + 1:]
    print(pre_weight_list)
    print(small)
    print(big)
    small_except = [i for i in small if i != 0]
    big_except = [i for i in small if i != 0]
    if small_except:
        pre_small = max(small)
    if big_except:
        pre_big = min(big)
    # print(pre_small)
    # print(pre_big)

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
    print(weight_list)
    print(len(weight_list))

    real = []
    if small_except and big_except:
        print(1)
        for i in weight_list:
            if pre_small <= i <= pre_big:
                real.append(i)
    elif small_except:
        print(2)
        for i in weight_list:
            if i >= pre_small:
                real.append(i)
    elif big_except:
        print(3)
        for i in weight_list:
            if i <= pre_big:
                real.append(i)
    else:
        print(4)
        for i in weight_list:
            real.append(i)
    print(real)
    print(len(real))
    print(max(real))



    # print(num)

    max_weight = max(weight_list)
    insert_loc = []
    for num, i in enumerate(weight_list):
        if i == max_weight:
            insert_loc.append(pos_loc[num])
    print(insert_loc)

    avail_loc_num = []
    for num, i in enumerate(insert_loc):
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