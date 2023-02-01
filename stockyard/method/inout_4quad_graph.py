import random
import pandas as pd
import copy
import math
from util import weight, check_maze, maze, order


def insert(block, map1, weight_map, count, area, df, flag, i, branch):
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


# def out(block, map1, count, flag):
#     if math.isnan(block.position_x):
#         return count
#     no_out = False
#     # print("반출 함수")
#     pos_loc = []
#     entrance_list = []  # 출고 가능 입구 리스트
#     width = block.width  # 가로 길이
#     height = block.height  # 세로 길이
#     x = block.position_x
#     y = block.position_y
#     x = int(x)
#     y = int(y)
#     start = (y, x)  # numpy 역전
#     map1.map[y:y + height, x:x + width] = 0
#     map1.map_color[y:y + height, x:x + width] = 0
#     s = maze.Maze(map1.map, width, height)
#     entrance_list.extend(s.find_start(flag))
#     # print(entrance_list)
#     pos_loc.extend(s.bfs(start))
#     # print(pos_loc)
#     for i in entrance_list:
#         if i in pos_loc:
#             # print("반출 가능")
#             no_out = False
#             break
#         else:
#             ################################################
#             # 출고 제약사항 여기서 작성
#             # print("바로 출고 불가능")
#             no_out = True
#
#     # 비용증가
#     if no_out:
#         # print("반출 불가")
#         count += 1
#     return count


def out(block, map1, count, flag, df, curr):
    test_map = copy.deepcopy(map1)

    if math.isnan(block.position_x):
        # print("문제 발생!!!")
        # print("반입 금지로 인한 반출X")
        # print(map1.block_num_map())
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
        # print("드가자 ")
        # print(num_map)
        # before = test_map.cv2_map()
        # before = cv2.resize(before, (600, 600), interpolation=cv2.INTER_NEAREST)
        # cv2.namedWindow('before', cv2.WINDOW_NORMAL)
        # cv2.imshow('before', before)
        # cv2.waitKey(0)
        obstruct_block_index = None

        obstruct_block = find_out(test_map.data, block, flag, test_map, num_map)

        if block.block_number in obstruct_block:
            obstruct_block.remove(block.block_number)

        # TODO 간섭 블록 어떻게 할지만 정해주면 됨
        for x in obstruct_block:

            # # 데이터 프레임 추가
            # print('현재 인덱스{}'.format(curr))
            # print('간섭블록{}'.format(x))
            # print(df)
            # temp = df.loc[df.block_number == x]
            # print(temp)
            # temp = temp.iloc[-1]
            # temp['date'] = df.loc[curr]['date']
            # temp['type'] = 1
            # temp1 = df[df.index <= curr]
            # temp2 = df[df.index > curr]
            # df = temp1.append(temp, ignore_index=True).append(temp2, ignore_index=True)
            # df.loc[curr + 1] = temp
            # print(df)
            # print("자 드가자", x)
            # print('현재 인덱스{}'.format(curr))
            # print('간섭블록{}'.format(x))
            # order.order(df)
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

            # print(map1.block_num_map())
            map1.data.pop(obstruct_block_index)

            erase_map(erase, map1)

            # order.order(df)

        count += len(obstruct_block)

    else:
        pass

    # map1.data.pop(curr_block_index)
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

            # # 블록들 제거
            # for num, i in enumerate(can_out_block):
            #     for index, j in enumerate(map1.data):  # 블록 데이터 pop
            #         if j['block_number'] == i['block_number']:
            #             map1.data.pop(index)

            num_map = map1.block_num_map()
            # print(num_map)
            # print(obstruct_dict)2
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