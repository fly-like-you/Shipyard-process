import numpy as np
import copy
import random
import matplotlib.pyplot as plt
import pandas as pd
from method import inout_2quad, inout_random, inout_depth, \
    inout_4quad, inout_new
from util import schedule, weight, plot, map_create, order, dataframe_modify
import argparse
from tqdm import tqdm
import time
import cv2
from method import out_block, out_block_not
from schdule_pearsonr import sche_pearson


pd.set_option('display.max_rows', 500)

SEED = 6
random.seed(SEED)
np.random.seed(SEED)
# numpy 옵션
np.set_printoptions(threshold=np.inf, linewidth=np.inf)


def random(df, new_map, flag, index, total_list, exist_block_num):
    curr = exist_block_num
    insert_cnt = 0
    area = 0
    out_cnt = 0
    start = time.time()

    while True:
        task = df.loc[curr]
        if task.type == 1:
            insert_cnt, area = inout_random.insert(task, new_map, flag, insert_cnt, area, df, exist_block_num)
        if task.type == 2:
            out_cnt, df = out_block_not.out(task, new_map, out_cnt, flag, df, curr)
        curr += 1
        # before = new_map.cv2_map()
        # before = cv2.resize(before, (600, 600), interpolation=cv2.INTER_NEAREST)
        # cv2.namedWindow('before', cv2.WINDOW_NORMAL)
        # cv2.imshow('before', before)
        # cv2.waitKey(0)
        if curr == len(df):
            break
    end = time.time()

    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)
    total_list[3][index].append(end-start)


def depth(df, new_map, flag, weight_map, index, total_list, exist_block_num):
    curr = exist_block_num
    insert_cnt = 0
    area = 0
    out_cnt = 0
    start = time.time()

    while True:
        task = df.loc[curr]
        if task.type == 1:
            insert_cnt, area = inout_depth.insert(task, new_map, weight_map, insert_cnt, area, df, flag, exist_block_num)
        if task.type == 2:
            out_cnt, df = out_block_not.out(task, new_map, out_cnt, flag, df, curr)
        curr += 1
        if curr == len(df):
            break
    end = time.time()

    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)
    total_list[3][index].append(end - start)


def quad2(df, new_map, flag, weight_map, index, total_list, exist_block_num):
    curr = exist_block_num
    insert_cnt = 0
    area = 0
    out_cnt = 0
    start = time.time()

    while True:
        task = df.loc[curr]
        if task.type == 1:
            print(1)
            insert_cnt, area = inout_2quad.insert(task, new_map, weight_map, insert_cnt, area, df, flag, exist_block_num)
        if task.type == 2:
            print(2)
            out_cnt, df = out_block_not.out(task, new_map, out_cnt, flag, df, curr)
        # before = new_map.cv2_map()
        # before = cv2.resize(before, (600, 600), interpolation=cv2.INTER_NEAREST)
        # cv2.namedWindow('before', cv2.WINDOW_NORMAL)
        # cv2.imshow('before', before)
        # cv2.waitKey(0)
        curr += 1
        if curr == len(df) - 1:
            break
    end = time.time()

    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)
    total_list[3][index].append(end - start)


def quad4(df, new_map, flag, weight_map, index, total_list, exist_block_num):
    curr = exist_block_num
    insert_cnt = 0
    area = 0
    out_cnt = 0
    start = time.time()

    while True:
        task = df.loc[curr]
        if task.type == 1:
            insert_cnt, area = inout_4quad.insert(task, new_map, weight_map, insert_cnt, area, df, flag,
                                                    curr, exist_block_num, branch=0)
        if task.type == 2:
            out_cnt, df = out_block_not.out(task, new_map, out_cnt, flag, df, curr)
        # before = new_map.cv2_map()
        # before = cv2.resize(before, (600, 600), interpolation=cv2.INTER_NEAREST)
        # cv2.namedWindow('before', cv2.WINDOW_NORMAL)
        # cv2.imshow('before', before)
        # cv2.waitKey(0)
        curr += 1
        if curr == len(df) - 1:
            break
    end = time.time()

    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)
    total_list[3][index].append(end - start)


def new(df, new_map, flag, weight_map, index, total_list, exist_block_num):
    curr = exist_block_num
    insert_cnt = 0
    area = 0
    out_cnt = 0
    start = time.time()

    while True:
        task = df.loc[curr]
        if task.type == 1:
            # print("in")
            insert_cnt, area = inout_new.insert(task, new_map, weight_map, insert_cnt, area, df, flag)
        if task.type == 2:
            # print("out")
            out_cnt, df = out_block.out(task, new_map, out_cnt, flag, df, curr)
        before = new_map.cv2_map()
        before = cv2.resize(before, (600, 600), interpolation=cv2.INTER_NEAREST)
        cv2.namedWindow('before', cv2.WINDOW_NORMAL)
        cv2.imshow('before', before)
        cv2.waitKey(0)
        curr += 1
        if curr == len(df) - 1:
            break
    end = time.time()

    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)
    total_list[3][index].append(end - start)

def user(df, new_map, flag, index, total_list, exist_block_num):
    '''


    total_list[0][index].append(insert_cnt)
    total_list[1][index].append(area)
    total_list[2][index].append(out_cnt)
    '''


def stockyard1(ax, param, epoch, flag, methods):
    # epoch, flag, methods = opt.epoch, opt.flag, opt.method
    param_block = param

    total_insert_cnt = [[] for _ in range(len(methods))]
    total_area = [[] for _ in range(len(methods))]
    total_out_cnt = [[] for _ in range(len(methods))]
    total_time = [[] for _ in range(len(methods))]

    total_list = [total_insert_cnt, total_area, total_out_cnt, total_time]

    for epoc in tqdm(range(epoch)):

        n_block = param_block[4]  # 기적치블록 개수
        block_number = 0  # 출고 순서 -> 나중에 스케줄에서 들고 와야함

        # 각 블록 정보 들어있는 리스트
        stockyard_list = []

        # 적치장 생성
        new_map = map_create.Map(param_block[0], param_block[1], flag, param_block[2], param_block[3])

        # weight 맵 생성
        weight_map = weight.create_weight(new_map.x_size, new_map.y_size, flag)
        # weight_map = weight.color(weight_map)

        # 블록 생성
        for k in range(n_block):
            stockyard_list.append(map_create.Block(new_map, weight_map, param_block[2], param_block[3],
                                                   block_number=k))
            block_number += 1

        # 기존 블록 개수 넘겨서 새 입고 블록 생성
        insert_block = schedule.exist_block(len(stockyard_list), param_block[2], param_block[3], param_block[5])
        total_insert_num = len(insert_block) + len(stockyard_list)

        # 스케쥴 생성해서 받아오기
        df = schedule.out_block(stockyard_list, insert_block, total_insert_num, param_block[6])
        df = df.fillna(value=0)
        # 스케줄 강제 설정
        # df = dataframe_modify.modify_df(df)
        # print(df)
        # sche_pearson(df)
        # 초기 최단거리 설정
        order.init_weight(new_map, weight_map, df, param_block[6])
        # print(df)

        # 스케줄 복사
        df_copy = [copy.deepcopy(df) for _ in range(len(methods))]

        # 맵 복사
        new_map_copy = [copy.deepcopy(new_map) for _ in range(len(methods))]

        # 함수 실행
        for index, method in enumerate(methods):
            if method == 'random':
                random(df_copy[index], new_map_copy[index], flag, index, total_list, n_block)
            if method == 'depth':
                depth(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list, n_block)
            if method == 'quad2':
                quad2(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list, n_block)
            if method == 'quad4':
                quad4(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list, n_block)
            if method == 'new':
                new(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list, n_block)
            if method == 'user':
                user(index, total_list, n_block)

    # 결과 출력
    for index, method in enumerate(methods):
        print(method)
        print("total_insert_avg =", np.mean(total_list[0][index]), np.std(total_list[0][index]))
        print("total_area_avg =", np.mean(total_list[1][index]), np.std(total_list[1][index]))
        print("total_out_avg = ", np.mean(total_list[2][index]), np.std(total_list[2][index]))
        print("total_time = ", np.mean(total_list[3][index]), np.std(total_list[3][index]))

    # plot
    label = [method for method in methods]
    x_list = total_list[2]  # total_out_cnt
    y_list = total_list[1]  # total_area
    plot.scatter(ax, x_list, y_list, label, flag, param)


def stockyard(ax, param):
    epoch, flag, methods = opt.epoch, opt.flag, opt.method
    param_block = param

    total_insert_cnt = [[] for _ in range(len(methods))]
    total_area = [[] for _ in range(len(methods))]
    total_out_cnt = [[] for _ in range(len(methods))]
    total_time = [[] for _ in range(len(methods))]

    total_list = [total_insert_cnt, total_area, total_out_cnt, total_time]

    for epoc in tqdm(range(epoch)):

        n_block = param_block[4]  # 기적치블록 개수
        block_number = 0  # 출고 순서 -> 나중에 스케줄에서 들고 와야함

        # 각 블록 정보 들어있는 리스트
        stockyard_list = []

        # 적치장 생성
        new_map = map_create.Map(param_block[0], param_block[1])

        # weight 맵 생성
        weight_map = weight.create_weight(new_map.x_size, new_map.y_size, flag)
        # weight_map = weight.color(weight_map)

        # 블록 생성
        for k in range(n_block):
            stockyard_list.append(map_create.Block(new_map, weight_map, param_block[2], param_block[3],
                                                   block_number=k))
            block_number += 1

        # 기존 블록 개수 넘겨서 새 입고 블록 생성
        insert_block = schedule.exist_block(len(stockyard_list), param_block[2], param_block[3], param_block[5])
        total_insert_num = len(insert_block) + len(stockyard_list)

        # 스케쥴 생성해서 받아오기
        df = schedule.out_block(stockyard_list, insert_block, total_insert_num, param_block[6])
        df = df.fillna(value=0)

        # 스케줄 복사
        df_copy = [copy.deepcopy(df) for _ in range(len(methods))]

        # 맵 복사
        new_map_copy = [copy.deepcopy(new_map) for _ in range(len(methods))]

        # 함수 실행
        for index, method in enumerate(methods):
            if method == 'random':
                random(df_copy[index], new_map_copy[index], flag, index, total_list, n_block)
            if method == 'depth':
                depth(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list, n_block)
            if method == 'quad2':
                quad2(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list, n_block)
            if method == 'quad4':
                quad4(df_copy[index], new_map_copy[index], flag, weight_map, index, total_list, n_block)
            if method == 'user':
                user(index, total_list, n_block)

    # 결과 출력
    for index, method in enumerate(methods):
        print(method)
        print("total_insert_avg =", np.mean(total_list[0][index]))
        print("total_area_avg =", np.mean(total_list[1][index]))
        print("total_out_avg = ", np.mean(total_list[2][index]))
        print("total_time = ", np.mean(total_list[3][index]))

    # plot
    label = [method for method in methods]
    x_list = total_list[2]  # total_out_cnt
    y_list = total_list[1]  # total_area
    plot.scatter(ax, x_list, y_list, label)


def sota(epoch=None, params=None, flag=None, methods=None):
    if epoch is None:
            epoch = 10

    if params is None:
        params = [[20, 20, 3, 7, 0, 100, 100]]
    
    for param in params:
        if param[0]**2 < param[4] * (param[3]**2):
            print('There is not enough stockyard space!!!')
            exit()


    if methods is None:
        methods = ['random']

    if flag is None:
        flag = [True, True, True, True]

    parameters = {'axes.labelsize': 7,
                  'axes.titlesize': 7,
                  'xtick.labelsize': 7,
                  'ytick.labelsize': 7,
                  'legend.fontsize': 7}
    plt.rcParams.update(parameters)

    fig = plt.figure(1)

    print("!!!start!!!")
    for j, flg in enumerate(flag):
        for i, param in enumerate(params):
            print('epoch {}'.format(epoch))
            print('param {}'.format(param))
            print('methods {}'.format(methods))
            print('flag {}'.format(flg))
            ax = fig.add_subplot(len(flag), len(params), len(params) * j + i + 1)
            stockyard1(ax, param, epoch, flg, methods)
    # plt.savefig("default.png")
    plt.savefig('{}{}.png'.format(flag, params))
    plt.show()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='stockyard test')
    parser.add_argument('--epoch', default=10, type=int)
    parser.add_argument('--params', default=[20, 20, 3, 7, 0, 100, 100], nargs='+', type=int, help='20 20 3 7 0 100 100')
    parser.add_argument('--flag', default=[True, True, True, True], nargs='+', type=bool, help='True True True True')
    parser.add_argument('--method', default=['random'], nargs='+', help='random, depth, quad2, quad4')
    opt = parser.parse_args()

    '''
    맵 텍스트 파일 업로드
    '''

    # 여러 파라미터 확인 하고 싶을 때
    # 적치장 가로 세로 , 블록 사이즈 범위, 기 적치 블록, 입고 블록 수, 출구 블록 수
    '''params = [[20, 30, 3, 4, 0, 30, 30],
              [20, 30, 3, 4, 15, 30, 30],
              [20, 30, 3, 7, 0, 30, 30],
              [20, 30, 3, 7, 0, 100, 100],
              [20, 40, 3, 7, 0, 100, 100],
              [40, 50, 3, 7, 0, 100, 100]]'''

    # 출입구 지정 위쪽, 왼쪽, 오른쪽, 아래쪽
    # flag = [True, True, True, True]

    parameters = {'axes.labelsize': 7,
                  'axes.titlesize': 7,
                  'xtick.labelsize': 7,
                  'ytick.labelsize': 7,
                  'legend.fontsize': 7}
    plt.rcParams.update(parameters)

    fig = plt.figure(1)
    params = [opt.params]

    for param in params:
        if param[0]**2 < param[4] * (param[3]**2):
            print('There is not enough stockyard space!!!')
            exit()

    print(opt)
    print("start")
    for i, param in enumerate(params):
        print('블록 파라미터{}'.format(param))
        ax = fig.add_subplot(1, len(params), i+1)
        stockyard(ax, param)

    plt.show()