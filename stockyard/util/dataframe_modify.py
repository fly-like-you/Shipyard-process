import pandas as pd


def modify_df(df):

    total_len = len(df)
    type = []
    block_number =[]
    a = [i for i in range(total_len//2)]
    for i in a:
        type.append(1)
        block_number.append(i)

    for i in a:
        type.append(2)
        block_number.append(i)

    # print(type)
    # print(block_number)
    # input()

    df['type'] = type

    df['block_number'] = block_number

    return df