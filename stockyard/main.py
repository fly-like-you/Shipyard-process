from generator import generator
from evaluate import evaluate
import pandas as pd
import random
import numpy as np

pd.set_option('display.max_rows', 500)

SEED = 3
random.seed(SEED)
np.random.seed(SEED)
# numpy 옵션
np.set_printoptions(threshold=np.inf, linewidth=np.inf)

params = [20, 30, 3, 7, 0, 100, 100]
flag = [True,True,True,True]

new_map, weight_map, new_df = generator(params, flag)

###
# modify_schdule
###

insert_cnt, out_cnt = evaluate(new_df, new_map, flag)