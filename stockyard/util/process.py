import random


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