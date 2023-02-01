import random
import copy
from datetime import timedelta


# 블록의 앞뒤 시간을 고려하여 이동가능한 블록 리스트 반환
def include_time(schedule, minutes):
    init_in_list = []
    minute_30 = timedelta(minutes=minutes)
    for a, date in enumerate(schedule['date']):
        temp = []
        # datetime_str = datetime.fromisoformat((str(date)))
        for b, include_time in enumerate(schedule['date']):
            if date - minute_30 < include_time < date + minute_30:
                temp.append(b)
        init_in_list.append(temp)

    return init_in_list


# 블록이 이동가능한 시간을 서로 고려하여 블록 리스트 반환
def include_or_time(schedule):
    init_in_list = []
    # 해당 블록이 이동가능한 인덱스 반환
    for a, task in enumerate(schedule.iterrows()):
        temp = []
        for b, include_time in enumerate(schedule['date']):
            if task[1]['date'] - timedelta(minutes=task[1]['allow_time']) < include_time < task[1]['date'] + timedelta(
                    minutes=task[1]['allow_time']):
                temp.append(b)

        init_in_list.append(temp)
    # 해당 블록이 이동가능해도 그에 맞는 블록이 불가능한 것 제거
    for i, k in enumerate(init_in_list):
        for j in k:
            if i not in init_in_list[j]:
                k.remove(j)

    return init_in_list


def check_schedule(schedule, include_schedule, df):
    df_copy = copy.deepcopy(df)
    check = True
    df_list = []
    # 중복 체크
    if len(schedule) != len(set(schedule)):
        check = False
        print('중복')
        return check

    # 허용 스케줄 체크
    for i in schedule:
        if i not in include_schedule[i]:
            check = False
            print('허용스케줄')
            return check

    # 반입 반출 순서 체크
    type_list = [df.loc[i]['type'] for i in schedule]
    block_number_list = [df.loc[i]['block_number'] for i in schedule]

    df_copy['type'] = type_list
    df_copy['block_number'] = block_number_list

    df_list = [[row['type'], row['block_number']] for idx, row in df_copy.iterrows()]

    for i, j in enumerate(df_list):
        for l, k in enumerate(df_list[i + 1:]):
            if j[1] == k[1]:
                if j[0] == 2:
                    check = False
                    print(i, j, l, k)
                    print('순서')
                    return check

    return check


def init_schedule(include_in):
    random_schedule = []
    while len(random_schedule) != len(include_in):
        random_schedule = []
        for i in include_in:
            choice_list = []
            for j in i:
                if j not in random_schedule:
                    choice_list.append(j)
            if len(choice_list) == 0:
                break
            else:
                random_schedule.append(random.choice(choice_list))

    return random_schedule