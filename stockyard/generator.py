from util import schedule, weight, map_create

# params [20, 20, 3, 7, 0, 100, 100] [적치장 가로 세로 , 블록 사이즈 범위, 기 적치 블록, 입고 블록 수, 출고 블록 수]
# flag = [True, True, True, True] [출입구 지정 위쪽, 왼쪽, 오른쪽, 아래쪽]
def generator(params, flag):

    if params[0]**2 < params[4] * (params[3]**2):
        print('There is not enough stockyard space!!!')
        exit()
            
    n_block = params[4]  # 기적치블록 개수
    block_number = 0  # 출고 순서 -> 나중에 스케줄에서 들고 와야함

    # 각 블록 정보 들어있는 리스트
    stockyard_list = []

    # 적치장 생성
    new_map = map_create.Map(params[0], params[1])

    # weight 맵 생성
    weight_map = weight.create_weight(new_map.x_size, new_map.y_size, flag)
    # weight_map = weight.color(weight_map)

    # 블록 생성
    for k in range(n_block):
        stockyard_list.append(map_create.Block(new_map, weight_map, params[2], params[3],
                                        block_number=k))
        block_number += 1

    # 기존 블록 개수 넘겨서 새 입고 블록 생성
    insert_block = schedule.exist_block(len(stockyard_list), params[2], params[3], params[5])
    total_insert_num = len(insert_block) + len(stockyard_list)

    # 스케쥴 생성해서 받아오기
    df = schedule.out_block(stockyard_list, insert_block, total_insert_num, params[6])
    df = df.fillna(value=0)

    return new_map, weight_map, df
