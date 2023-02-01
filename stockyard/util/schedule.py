import pandas as pd
import numpy as np
import random
import time


# pd.set_option("display.max_rows", None, "display.max_columns", None)


def str_time_prop(start, end, format):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    prop = random.random()
    delta = prop * (etime - stime)
    if delta < 300:  # 입고 출고 최소 시간 간격 유지
        delta = 300
    ptime = stime + delta

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p')


def str_time_normal_prop(start, end, format):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    mean = (etime - stime) / 2

    while True:
        # 상관계수 조절 mu 0 -> 1 2 -> -1
        value = np.random.normal(0, 0.1, 1)
        # print(value)
        delta = mean + mean * value[0]
        # print(delta)
        ptime = stime + delta
        # print(stime)
        # print(ptime)
        # print(1)
        # print(time.strftime(format, time.localtime(stime)))
        # print(time.strftime(format, time.localtime(ptime)))
        # input()
        if ptime > stime:
            break

    # print(time.strftime(format, time.localtime(stime)))
    # print(time.strftime(format, time.localtime(ptime)))
    # input()
    return time.strftime(format, time.localtime(ptime))


def random_normal_date(start, end):
    return str_time_normal_prop(start, end, '%m/%d/%Y %I:%M %p')


class InsertBlockCreate:  # 입고 블록 생성
    block_number = 0  # 블록 번호

    def __init__(self, min_size, max_size):
        self.type = 1  # 입고 블록

        # min_size = 3  # 사이즈 결정
        # max_size = 7

        self.position_x = None  # 나중 적치 되면 업데이트 되게 해라
        self.position_y = None

        self.width = random.randint(min_size, max_size)
        self.height = random.randint(min_size, max_size)

        self.block_number = InsertBlockCreate.block_number
        InsertBlockCreate.block_number += 1
        self.date = random_date("10/12/2020 6:00 AM", "10/12/2020 6:00 PM")  # 날짜 조절
        self.weight_val = None


def exist_block(block_list, min_size, max_size, block_num):  # 새 입고 블록 생성 함수
    new_insert_block = []  # 적치 블록 정보 리스트
    InsertBlockCreate.block_number = block_list  # 기존 적치 블록 부터 번호 생성
    block_num = block_num  # 적치할블록 개수
    for i in range(block_num):
        new_insert_block.append(InsertBlockCreate(min_size, max_size))
    return new_insert_block


def out_block(stockyard_list, insert_block, total_insert_num, choice_num):  # 출고 블록 선택 함수
    df = pd.DataFrame(columns=('type', 'position_x', 'position_y', 'width', 'height',
                               'block_number', 'date', 'weight_val'))
    df = df.astype({'type': int, 'position_x': int, 'position_y': int, 'block_number': int})
    out_block_num = []
    out_block_list = []
    choice_num = choice_num  # 꺼낼 블록 갯수
    # print("총 입고 블록 갯수=", total_insert_num)
    num = random.randrange(0, total_insert_num)
    for i in range(choice_num):  # 꺼낼 블록 번호 리스트
        while num in out_block_num:
            num = random.randrange(0, total_insert_num)
        out_block_num.append(num)
    # print(" 반출 블록 번호= ", out_block_num)

    exist_block_num = [i.block_number for i in stockyard_list]
    insert_block_num = [i.block_number for i in insert_block]
    # print(" 반입 블록 번호= ", insert_block_num)

    for i in out_block_num:  # 기존 적치면 시간 생성 랜덤 아니면 시간 보고 해야 되니깐

        if i in exist_block_num:  # 기존 적치 블록인가
            x = exist_block_num.index(i)
            out_block_list.append(OutBlockCreate(stockyard_list[x]))

        if i in insert_block_num:  # 새로 들어오는 블록인가
            x = insert_block_num.index(i)
            out_block_list.append(OutBlockCreate(insert_block[x]))

    '''for i in stockyard_list:  # 스케줄 등록
        dict_data = pd.Series(i.__dict__)
        df = df.append(pd.Series(dict_data), ignore_index=True)'''

    for i in stockyard_list:
        dict_data = pd.Series(i.__dict__)
        # print(dict_data)
        df = df.append(pd.Series(dict_data), ignore_index=True)

    for i in insert_block:  # 스케줄 등록
        dict_data = pd.Series(i.__dict__)
        # print(dict_data)
        df = df.append(pd.Series(dict_data), ignore_index=True)

    for i in out_block_list:  # 스케줄 등록
        dict_data = pd.Series(i.__dict__)
        # print(dict_data)
        df = df.append(pd.Series(dict_data), ignore_index=True)

    # df_sorted = df.sort_values(by='date', key=lambda x: time.strptime(x, '%m/%d/%Y %I:%M %p'))\
    #    .reset_index(drop=True) # 가능하면 하자
    # df.astype({'date': str})
    # print(df.dtypes)

    # date 별로 정렬
    df["date"] = pd.to_datetime(df["date"])
    df_sorted = df.sort_values(by='date').reset_index(drop=True)

    # 출고가 먼저 앞에 올 때 swap
    df_list = [[row['type'], row['block_number']] for idx, row in df_sorted.iterrows()]

    for i, j in enumerate(df_list):
        for l, k in enumerate(df_list[i + 1:]):
            if j[1] == k[1]:
                if j[0] == 2:
                    temp = df_sorted.iloc[i].copy()
                    df_sorted.iloc[i] = df_sorted.iloc[i+l+1]
                    df_sorted.iloc[i+l+1] = temp

    return df_sorted


class OutBlockCreate:  # 출고 블록 랜덤 생성 클래스
    def __init__(self, block):
        self.type = 2  # 출고 타입
        self.position_x = block.position_x
        self.position_y = block.position_y
        self.width = block.width
        self.height = block.height
        self.block_number = block.block_number
        self.weight_val = block.weight_val
        self.date = None
        if block.date is None:
            self.date = random_date("10/12/2020 6:00 AM", "10/12/2020 6:00 PM")
        else:
            self.date = random_date(block.date, "10/12/2020 6:00 PM")
