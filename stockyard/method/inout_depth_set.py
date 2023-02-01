import random
import pandas as pd
import math
import copy
from util import weight, check_maze, maze, order


def insert(block, map1, weight_map, count, area, df, flag):
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


def out(block, map1, count, flag, df, curr):
    test_map = copy.deepcopy(map1)
    test_map_copy = copy.deepcopy(map1)

    if math.isnan(block.position_x):
        # print("문제 발생!!!")
        # print("반입 금지로 인한 반출X")
        # print(map1.block_num_map())
        # print(df)
        # print(block)
        # input()
        return count, df

    curr_block_index = None

    for index, j in enumerate(test_map.data):  # 블록 데이터 pop
        if j['block_number'] == block.block_number:
            curr_block_index = index
    # 밑에 계산 때문에 잠시 제외
    map1.data.pop(curr_block_index)
    test_map.data.pop(curr_block_index)
    test_map_copy = copy.deepcopy(map1)

    obstruct_block_list = []
    obstruct_block = []
    best_obstruct_block = []

    no_out = out_check(block, test_map, flag, 1)
    while no_out:
        block_list = test_map.data
        no_out_list = []
        can_out_block = []
        # 바로 나갈수 있는 블록 탐색
        for i in block_list:
            no_out = out_check(i, test_map, flag, 1)  # 블록들마다 나올수 있는지 체크
            if no_out is False:
                can_out_block.append(i)

        # 나갈 수 있는 블록들 추가 될때 마다 교집합 추가
        if not obstruct_block_list:
            for i in can_out_block:
                obstruct_block_list.append([i])
        else:
            z = []
            for i in obstruct_block_list:
                for j in can_out_block:
                    temp_list = copy.deepcopy(i)
                    temp_list.append(j)
                    z.append(temp_list)
            obstruct_block_list = z

        # 블록 집합들 차례로 제거 했을 때 나갈수 있는지 체크
        for i in obstruct_block_list:
            for j in i:
                erase_map(j, test_map_copy)
            no_out = out_check(block, test_map_copy, flag, 1)
            no_out_list.append(no_out)
            for j in i:
                draw_map(j, test_map_copy)

        # 현재 블록 나갈 수 있으면 그 집합들 추가 불가능시 블록 제거 후 다음 블록 탐색 준비
        if False in no_out_list:
            for i, j in enumerate(no_out_list):
                if j is False:
                    obstruct_block.append(obstruct_block_list[i])

            # TODO 어떻게 선택할껀데
            x_axis, y_axis = order.order(df)

            # 가장 늦게 나가는 그룹 선택
            rank_list = []
            for k in obstruct_block:
                temp = []
                for m in k:
                    if m['block_number'] in y_axis:
                        temp.append(y_axis.index(m['block_number']))
                    else:
                        temp.append(len(y_axis))
                rank_list.append(temp)
            best_rank_list = [sum(i)/len(i) for i in rank_list]
            best_rank = best_rank_list.index(max(best_rank_list))
            best_obstruct_block = obstruct_block[best_rank]
            # best_obstruct_block = random.choice(obstruct_block)

            no_out = False

        else:
            for num, i in enumerate(can_out_block):
                erase_map(i, test_map)
                for index, j in enumerate(test_map.data):  # 블록 데이터 pop
                    if j['block_number'] == i['block_number']:
                        test_map.data.pop(index)

    erase_map(block, map1)

    if best_obstruct_block:
        for x in best_obstruct_block:
            for index, j in enumerate(map1.data):  # 블록 데이터 pop
                if j['block_number'] == x['block_number']:
                    temp = pd.DataFrame(map1.data[index], index=[0])
                    erase = pd.Series(map1.data[index])
                    temp['date'] = df.loc[curr]['date']
                    temp['type'] = 1
                    temp1 = df[df.index <= curr]
                    temp2 = df[df.index > curr]
                    df = pd.concat([temp1, temp], axis=0, ignore_index=True)
                    df = pd.concat([df, temp2], axis=0, ignore_index=True)
                    map1.data.pop(index)
                    erase_map(erase, map1)

        count += len(best_obstruct_block)
        return count, df

    else:
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


# 간섭 블록 리스트 생성
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

        # 다시 해당 블록 나올수 있는지 검사
        no_out = out_check(block, map1, flag, 1)

        # can_out_block_list.append(can_out_block)

        if no_out:
            # print(num_map)
            # before = map1.cv2_map()
            # before = cv2.resize(before, (600, 600), interpolation=cv2.INTER_NEAREST)
            # cv2.namedWindow('before', cv2.WINDOW_NORMAL)
            # cv2.imshow('before', before)
            # cv2.waitKey(0)
            # block list 업데이트
            block_list = cant_out_block
            # print(block_list)
            # print(can_out_block)
            # print(df)

            # 바로 나갈 수 있는 블록들 제거
            for num, i in enumerate(can_out_block):
                for index, j in enumerate(map1.data):  # 블록 데이터 pop
                    if j['block_number'] == i['block_number']:
                        map1.data.pop(index)

            # 다시 바로 나갈수있는 애들만 추리기
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

            # # 블록들 제거
            # for num, i in enumerate(can_out_block):
            #     for index, j in enumerate(map1.data):  # 블록 데이터 pop
            #         if j['block_number'] == i['block_number']:
            #             map1.data.pop(index)

            num_map = map1.block_num_map()
            # print(num_map)
            # print(obstruct_dict)
            # print(block)
            # input()

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

            # print(obstruct_block_list)
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
