from transporter.data.create_data.FileManager import FileManager
from transporter.transporter.GA_refactoring.GA_refactoring import GA
from transporter.data.create_data.Graph import Graph
import pandas as pd
import os

ga_params = {
    'POPULATION_SIZE': 100,
    'GENERATION_SIZE': 500,
    'ELITISM_RATE': 0.05,
    'MUTATION_RATE': 0.1,
    'SELECTION_METHOD': 'selection2',
}
precondition = {
    'START_TIME': 9,  # 전제
    'FINISH_TIME': 18,  # 전제
    'LOAD_REST_TIME': 0.3,  # 전제
    'BLOCKS': 100,  # 전제
}
def get_dir_path(target):
    file_path = os.getcwd()
    target_dir = target

    # 경로를 분할합니다.
    path_parts = os.path.normpath(file_path).split(os.sep)

    # 특정 디렉터리까지의 인덱스를 찾습니다.
    index = path_parts.index(target_dir)

    # 해당 인덱스까지의 경로를 조합합니다.
    target_path_parts = path_parts[:index + 1]

    # 드라이브 문자와 경로를 올바르게 결합합니다.
    if os.name == 'nt' and len(target_path_parts[0]) == 2:  # 윈도우 드라이브 문자 (예: C:)
        target_path = os.path.join(target_path_parts[0] + os.sep, *target_path_parts[1:])
    else:
        target_path = os.path.join(*target_path_parts)

    return target_path

def random_search(num_samples=30):
    results = []

    for i in range(num_samples):
        print(f"{i+1}번째 데이터분석")

        ga = GA(transporter_container, block_container, graph, ga_params, precondition)
        ga_result = ga.run_GA()
        score = ga_result['best_fitness']
        distance = ga_result['best_distance']
        # 모델 학습 및 평가
        results.append({
            'fitness': score,
            'distance': distance
        })
        print(f"최고 점수 {score}")

    # 결과를 score를 기준으로 내림차순으로 정렬한 데이터프레임 반환
    df_results = pd.DataFrame(results).sort_values(by='fitness', ascending=False)

    # 데이터프레임을 pickle 파일로 저장
    df_results.to_pickle(f"GA_{cluster}_{ga_params['GENERATION_SIZE']}_len30.pkl")


cluster = "cluster2"
data_path = os.path.join(get_dir_path("transporter"), "data")
node_file_path = os.path.join(data_path, "nodes_and_blocks", "cluster", "simply_mapping", f"node({cluster}).csv")
transporter_path = os.path.join(data_path, 'transporters', 'transporter.csv')
block_path = os.path.join(data_path, "nodes_and_blocks", "cluster", "simply_mapping", f"block({cluster}).csv")


if __name__ == "__main__":
    results = []

    filemanager = FileManager()
    graph = Graph(node_file_path)
    transporter_container = filemanager.load_transporters(transporter_path)
    block_container = filemanager.load_block_data(block_path)
    random_search()

