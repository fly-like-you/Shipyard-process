import numpy as np


def create_weight(x, y, flag):
    result = None
    up = np.linspace(np.zeros(x), np.full((1, x), y - 1)[0], y)
    left = np.linspace(np.zeros(y), np.full((1, y), x - 1)[0], x).T
    right = np.flip(left)
    down = np.flip(up)
    a = [up, left, right, down]

    for i in range(4):
        if flag[i]:
            if result is None:
                result = a[i]
            else:
                result = np.where(result > a[i], a[i], result)

    return result


def color(map):
    map = map / 9
    return map


def weight_cal(pos_loc, weight_map, height, width):
    weight_list = [weight_map[i[0]:i[0]+height, i[1]:i[1]+width].mean() for i in pos_loc]
    return weight_list


if __name__ == '__main__':
    flag = [True, True, False, False]
    result = create_weight(15, 20, flag)
    print(result)
    print(result[0:4, 0:4].sum())