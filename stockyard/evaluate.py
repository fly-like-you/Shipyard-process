from method import inout_random
from util import maze, check_maze
import copy
import math
import pandas as pd
import random


def evaluate(df, new_map, flag):

    curr = 0
    insert_cnt = 0
    out_cnt = 0

    while True:
        task = df.loc[curr]
        if task.type == 1:
            insert_cnt = insert(task, new_map, insert_cnt)
        if task.type == 2:
            out_cnt, df = inout_random.out(task, new_map, out_cnt, flag, df, curr)
        curr += 1
        if curr == len(df):
            break

    return insert_cnt, out_cnt


def insert(block, map1, count):
    minsize = 50
    maxsize = 255
    insert_loc_x = block.position_x
    insert_loc_y = block.position_y
    h_yard = block.width  # 가로 길이
    v_yard = block.height  # 세로 길이
    ran_num = random.randint(minsize, maxsize)  # 블록 색깔
    
    if insert_loc_x is None and insert_loc_y is None:
        count += 1
        return count
    else:
        if 1 in map1.map[insert_loc_y:insert_loc_y + v_yard, insert_loc_x:insert_loc_x + h_yard]:
            raise Exception("block exist in yard")

    map1.map[insert_loc_y:insert_loc_y + v_yard, insert_loc_x:insert_loc_x + h_yard] = 1
    map1.map_color[insert_loc_y:insert_loc_y + v_yard, insert_loc_x:insert_loc_x + h_yard] = ran_num

    block_data = block.to_dict()  # 블록 데이터 가공
    block_data['position_x'] = insert_loc_x
    block_data['position_y'] = insert_loc_y

    map1.block_data(block_data)

    return count


def out(block, map1, count, flag, df, curr):
    test_map = copy.deepcopy(map1)

    if math.isnan(block.position_x):
        # print("문제 발생!!!")
        # print("반입 금지로 인한 반출X")
        # print(df)
        # print(block)
        # input()
        return count, df

    curr_block_index = None
    num_map = test_map.block_num_map()

    for index, j in enumerate(test_map.data):  # 블록 데이터 pop
        if j['block_number'] == block.block_number:
            curr_block_index = index
    # print(block)
    # print(num_map)
    # print(df)

    map1.data.pop(curr_block_index)

    test_map.data.pop(curr_block_index)  # 밑에 계산 때문에 잠시 제외

    # width, height, x, y = trans_data(block)
    no_out = out_check(block, test_map, flag, 1)

    # 비용증가
    if no_out:

        obstruct_block_index = None

        obstruct_block = find_out(test_map.data, block, flag, test_map, num_map)

        if block.block_number in obstruct_block:
            obstruct_block.remove(block.block_number)

        for x in obstruct_block:
            # 데이터 삭제
            for index, j in enumerate(map1.data):  # 블록 데이터 pop
                if j['block_number'] == x:
                    obstruct_block_index = index
            # print('현재 인덱스{}'.format(curr))
            # print('간섭블록{}'.format(x))
            temp = pd.DataFrame(map1.data[obstruct_block_index], index=[0])
            erase = pd.Series(map1.data[obstruct_block_index])
            temp['date'] = df.loc[curr]['date']
            temp['type'] = 1
            temp1 = df[df.index <= curr]
            temp2 = df[df.index > curr]
            df = pd.concat([temp1, temp], axis=0, ignore_index=True)
            df = pd.concat([df, temp2], axis=0, ignore_index=True)

            map1.data.pop(obstruct_block_index)

            erase_map(erase, map1)

        count += len(obstruct_block)

    else:
        pass

    erase_map(block, map1)

    return count, df


# 블록 데이터와 맵 만 들어가면 안에 곁에 있는거 빼주고 맵을 반
# 나갈수 있는 블록인지만 체크지
def out_check(block, copy_map, flag, point):
    # print("check", block)
    no_out = False
    pos_loc = []
    entrance_list = []  # 출고 가능 입구 리스트
    width, height, x, y = trans_data(block)

    x = int(x)
    y = int(y)
    start = (y, x)  # numpy 역전

    copy_map.map[y:y + height, x:x + width] = 0
    copy_map.map_color[y:y + height, x:x + width] = 0

    s = maze.Maze(copy_map.map, width, height)
    entrance_list.extend(s.find_start(flag))
    pos_loc.extend(s.bfs(start))

    if not pos_loc:  # 자기 자신밖에 없으면 자신 추가
        pos_loc.append(start)

    if point == 1:
        minsize = 50
        maxsize = 255
        random_num = random.randint(minsize, maxsize)
        copy_map.map[y:y + height, x:x + width] = 1
        copy_map.map_color[y:y + height, x:x + width] = random_num

    for i in entrance_list:  # 입구리스트에
        if i in pos_loc:  # 이동 가능 경로가 있으면
            # print("반출 가능")
            no_out = False
            break
        else:
            # print("바로 출고 불가능")
            no_out = True

    return no_out


def find_out(block_list, block, flag, map, num_map):
    map1 = copy.deepcopy(map)
    num_map = num_map
    obstruct_dict = {}
    obstruct_block_list = set()

    while True:

        no_out_list = []
        for i in block_list:
            no_out = out_check(i, map1, flag, 1)  # 블록들마다 나올수 있는지 체크
            no_out_list.append(no_out)

        can_out_list = [index for index, j in enumerate(no_out_list) if j is False]  # 바로 나올수 있는 블록 인덱스
        cant_out_list = [index for index, j in enumerate(no_out_list) if j is True]  # 바로 나올수 없는 블록 인덱스
        can_out_block = [block_list[i] for i in can_out_list]
        cant_out_block = [block_list[i] for i in cant_out_list]

        for i in can_out_block:
            erase_map(i, map1)

        # 다시 블록들 나올수 있는지 검사
        no_out = out_check(block, map1, flag, 1)

        # can_out_block_list.append(can_out_block)

        if no_out:
            # block list 업데이트
            block_list = cant_out_block
            # 블록들 제거
            for num, i in enumerate(can_out_block):
                for index, j in enumerate(map1.data):  # 블록 데이터 pop
                    if j['block_number'] == i['block_number']:
                        map1.data.pop(index)

            # 진짜 나갈수있는 애들만 추리기
            no_out_list = []
            for i in cant_out_block:
                no_out = out_check(i, map1, flag, 1)
                no_out_list.append(no_out)

            can_out_list = [index for index, j in enumerate(no_out_list) if j is False]
            can_out_block = [block_list[i] for i in can_out_list]

            # 각 블록 간섭블록 집합 구하기
            for num, i in enumerate(can_out_block):
                width, height, x, y = trans_data(i)
                number = i['block_number']
                x = int(x)
                y = int(y)
                start = (y, x)  # numpy 역전
                erase_map(i, map1)
                check = check_maze.CheckMaze(map1, width, height, num_map, start)
                check.dijkstra(start)
                obstruct_block = check.best_obstruct_block(flag)

                for x in obstruct_block.copy():
                    if x in obstruct_dict:
                        obstruct_block.update(obstruct_dict[x])

                obstruct_dict[number] = obstruct_block

                draw_map(i, map1)

            num_map = map1.block_num_map()

        else:
            width, height, x, y = trans_data(block)
            x = int(x)
            y = int(y)
            start = (y, x)  # numpy 역전
            erase_map(block, map1)
            check = check_maze.CheckMaze(map1, width, height, num_map, start)
            check.dijkstra(start)
            obstruct_block = check.best_obstruct_block(flag)
            obstruct_block_list.update(obstruct_block)

            for x in obstruct_block.copy():
                if x in obstruct_dict:
                    obstruct_block_list.update(obstruct_dict[x])
                else:
                    pass

            break

    return obstruct_block_list


def trans_data(block):
    width = block['width']  # 가로 길이
    height = block['height']  # 세로 길이
    x = block['position_x']
    y = block['position_y']

    return int(width), int(height), int(x), int(y)


def draw_map(block, map):
    width, height, x, y = trans_data(block)
    random_num = random.randint(50, 255)
    map.map[y:y + height, x:x + width] = 1
    map.map_color[y:y + height, x:x + width] = random_num


def erase_map(block, map):
    width, height, x, y = trans_data(block)
    map.map[y:y + height, x:x + width] = 0
    map.map_color[y:y + height, x:x + width] = 0
