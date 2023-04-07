import os
import random

from transporter.transporter.GA_refactoring.GA_refactoring import GA
from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.create_data.Graph import Graph
import pandas as pd

node_file_path = os.path.join(os.getcwd(), '..', "create_data", "data", "node.csv")
transporter_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'transporter.csv')
block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'Blocks.csv')
filemanager = FileManager()


precondition = {
    'START_TIME': 9,  # 전제
    'FINISH_TIME': 18,  # 전제
    'LOAD_REST_TIME': 0.3,  # 전제
    'BLOCKS': 100,  # 전제
}

graph = Graph(node_file_path)
transporter_container = filemanager.load_transporters(transporter_path)
block_container = filemanager.load_block_data(block_path, precondition['BLOCKS'])

def random_search(config_dict, num_samples=300):
    results = []

    for i in range(num_samples):
        print(f"{i+1}번째 데이터분석")
        # 랜덤하게 하이퍼파라미터 샘플링
        params = {param: random.uniform(config_dict[param]['min'], config_dict[param]['max']) for param in config_dict}
        params['SELECTION_METHOD'] = random.choice(['selection2', 'roulette'])
        params['POPULATION_SIZE'] = int(params['POPULATION_SIZE'])
        params['GENERATION_SIZE'] = int(params['GENERATION_SIZE'])

        ga = GA(transporter_container, block_container, graph, params, precondition)
        score = ga.run_GA()['best_fitness']
        # 모델 학습 및 평가
        results.append({
            'fitness': score,
            'params': params,
        })
        print(f"최고 점수 {score}")

    # 결과를 score를 기준으로 내림차순으로 정렬한 데이터프레임 반환
    df_results = pd.DataFrame(results).sort_values(by='fitness', ascending=False)

    # 데이터프레임을 pickle 파일로 저장

    # 최적의 조합 반환
    best_params = df_results.iloc[0]['params']

    df_results.to_pickle(f"ELITISM-{round(best_params['ELITISM_RATE'],3)}MUTATION-{round(best_params['MUTATION_RATE'],3)}.pkl")

    return best_params

if __name__ == "__main__":

    ga_params = {
        'POPULATION_SIZE': {'min': 100, 'max': 100},
        'GENERATION_SIZE': {'min': 1000, 'max': 1000},
        'ELITISM_RATE': {'min': 0.05, 'max': 0.3},
        'MUTATION_RATE': {'min': 0.05, 'max': 0.05},
    }

    print(random_search(ga_params))


