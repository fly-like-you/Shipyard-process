import random
import numpy as np
import copy
from util import weight
from util.schedule import random_date


class Map:
    def __init__(self, min_size, max_size, flag, block_min_size, block_max_size, x_size=None, y_size=None):
        self.x_size = None
        self.y_size = None
        self.block_min_size = block_min_size
        self.block_max_size = block_max_size
        self.side_size = 1  # 출입구 크기
        self.map = None
        self.stackyard = []
        self.data = []
        self.flag = flag
        self.y_order = None
        self.weight = None
        self.block_relation = None
        # min_size = 20  # 20
        # max_size = 30  # 30

        if x_size is not None:
            self.x_size = x_size
        else:
            self.x_size = random.randint(min_size, max_size)

        if y_size is not None:
            self.y_size = y_size
        else:
            self.y_size = random.randint(min_size, max_size)

        self.map = np.zeros((self.x_size, self.y_size))
        self.map = self.map.T
        self.num_map = None
        self.map_color = copy.deepcopy(self.map)
        # print('map', self.map.shape)
        #  self.map[:, -1] = 0  # 출입구 100 set

        # print('적치장 {} x {} 크기 생성'.format(str(self.x_size), str(self.y_size)))

    # 블록 그리기
    def map_draw(self, block=None):
        if block is not None:
            x_start = block.position_x
            x_end = block.position_x + block.width
            y_start = block.position_y
            y_end = block.position_y + block.height
            self.map[y_start:y_end, x_start: x_end] = 1

    def map_draw_color(self, block=None):
        if block is not None:
            x_start = block.position_x
            x_end = block.position_x + block.width
            y_start = block.position_y
            y_end = block.position_y + block.height
            self.map_color[y_start:y_end, x_start: x_end] = 255

    def setstackyard(self, count):
        for _ in range(count):
            self.stackyard.append(Block(self))

    def cv2_map(self):
        # return (self.map * 255).astype('uint8')
        return self.map_color.astype('uint8')

    def flip(self):
        self.map = np.fliplr(self.map)

    def block_data(self, block):  # 적치장에 블록 데이터 저장
        self.data.append(block)

    def position_set(self, block, x, y):
        block.position_x = x
        block.position_y = y
        self.data.append(block)

    # 블록 데이터에서 새로 블록 번호 맵을 만들어 줌
    def block_num_map(self):
        self.num_map = np.full((self.y_size, self.x_size), 999)
        for i in self.data:
            position_x = i['position_x']
            position_y = i['position_y']
            width = i['width']
            height = i['height']
            block_num = i['block_number']
            for j in range(position_x, position_x + width):
                for k in range(position_y, position_y + height):
                    self.num_map[k][j] = block_num
        # print(self.num_map)

        return self.num_map

    # def __repr__(self):
    #     return "적치장 크기 = " + str(self.getX_size()) + "m X " + str(self.getY_size()) + "m ."


class Block:
    def __init__(self, map, weight_map, min_size, max_size, block_number=None, position_x=None, position_y=None, width=None, height=None,
                 side_size=1, type=None):  # 나중에 type 지워라
        global position_x_list, position_y_list
        self.type = 1  # 입고 블록
        self.position_x = None  # 나중에 스케쥴표에서 받아오기
        self.position_y = None
        self.width = None  # 높이
        self.height = None  # 폭
        self.block_number = block_number
        # self.date = None
        self.date = random_date("10/11/2020 6:00 AM", "10/11/2020 6:00 PM")
        self.weight_val = None
        # print("weight map", weight_map.shape)
        # print("map", map.map.shape)

        # min_size = 3  # 3
        # max_size = 7  # 4
        count = 0

        # if type == 2:
        #     self.width = random.randint(min_size, max_size)
        #     self.height = random.randint(min_size, max_size)
        #     pass

        while True:
            if width is not None:
                self.width = width
            else:
                self.width = random.randint(min_size, max_size)

            if height is not None:
                self.height = height
            else:
                self.height = random.randint(min_size, max_size)

            # min_position = side_size
            min_position = 0
            max_x_position = map.x_size - self.width
            # max_x_position = map.x_size - self.width - side_size
            max_y_position = map.y_size - self.height  # 출입구 오른쪽 한쪽만 가정
            # max_y_position = map.y_size - self.height - side_size
            # TODO initialize code refactoring
            if count > 100:  # 제일 안에 배치하는게 빡세면 그만
                if position_x is not None:
                    if position_x > max_x_position:
                        position_x = max_x_position
                        print(" 적치장 X 위치 값 오류 ")

                    self.position_x = position_x
                else:
                    position_x_list = [random.randint(min_position, max_x_position) for _ in range(10)]
                    # self.position_x = random.randint(min_position, max_x_position)

                if position_y is not None:
                    if position_y > max_y_position:
                        position_y = max_y_position
                        print(" 적치장 Y 위치 값 오류 ")

                    self.position_y = position_y
                else:
                    position_y_list = [random.randint(min_position, max_y_position) for _ in range(10)]
                    # self.position_y = random.randint(min_position, max_y_position)
                pos_list = [(position_y_list[i], position_x_list[i]) for i in range(10)]  # bfs 에서 numpy 안써서
                # print("pos_list", pos_list)

                weight_list = weight.weight_cal(pos_list, weight_map, self.height, self.width)
                # print(weight_list)
                insert_loc = pos_list[weight_list.index(max(weight_list))]
                # print(insert_loc)
                self.position_x = insert_loc[1]  # inout 함수 참조
                self.position_y = insert_loc[0]

            else:
                self.position_x = random.randint(min_position, max_x_position)
                self.position_y = random.randint(min_position, max_y_position)

            x_end = self.position_x + self.width
            y_end = self.position_y + self.height
            # 적치장이 현재 위치하려는 곳에 없으면 생성
            if all(x not in map.map[self.position_y:y_end, self.position_x:x_end] for x in [1, 999]):
                # print(insert_loc)
                # if 1 and 100 not in map.map[self.position_y:y_end, self.position_x:x_end]:
                self.weight_val = weight_map[self.position_y:y_end, self.position_x:x_end].mean()
                map.map_draw(block=self)
                map.map_draw_color(block=self)
                # print( map.map[self.position_x:x_end, self.position_y:y_end])
                break
            else:
                count += 1
        ################
        map.block_data(block=self.__dict__)  # 블록 데이터 저장
        ################

    def color(self, map):
        x_end = self.position_x + self.width
        y_end = self.position_y + self.height
        map[self.position_y:y_end, self.position_x:x_end] = 125
        return map

    def position_set(self, x, y):
        self.position_x = x
        self.position_y = y

    # def __repr__(self):
    #     return "x,y 좌표 %s,%s" % (self.position_x, self.position_y)