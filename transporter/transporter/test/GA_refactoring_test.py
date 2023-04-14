import os
import unittest
from transporter.transporter.GA_refactoring.GA_refactoring import GA
from transporter.transporter.create_data.FileManager import FileManager
from transporter.transporter.create_data.Graph import Graph

# 박준호가 작성한 GA_refactoring 파일의 코드를 테스트하는 코드입니다.
node_file_path = os.path.join(os.getcwd(), '..', "create_data", "data", "node(cluster3).csv")
block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'blocks.csv')
transporter_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'transporter.csv')

config_dict = {
    'POPULATION_SIZE': 10,  # 한 세대에서의 인구 수를 설정합니다.
    'GENERATION_SIZE': 10,  # 몇 세대에 걸쳐 진화할 지 설정합니다.
    'LOAD_REST_TIME': 0.2,  # 트랜스포터가 목적지에서 물건을 실어나르는 시간을 설정합니다 (시)
    'ELITISM_RATE': 0.5,  # 엘리트 individual의 비율을 결정합니다.
    'MUTATION_RATE': 0.4,  # 돌연변이가 일어날 확률을 설정합니다.
    'START_TIME': 9,  # 일과의 시작시간을 결정합니다.
    'FINISH_TIME': 18,  # 일과가 끝나는 시간을 결정합니다.
    'BLOCKS': 100,  # 총 블록 수를 설정합니다. 최대 100개까지 설정가능합니다.
}


class MyTestCase(unittest.TestCase):
    file_manager = FileManager()
    graph = Graph(node_file_path)
    transporter_container = file_manager.load_transporters(transporter_path)
    block_container = file_manager.create_block_from_graph_file(node_file_path, 100)

    ga = GA(transporter_container, block_container, graph, config_dict, selection_method='square_roulette')
    best_individual = ga.run_GA()['best_individual']


    def test_generate_population(self):  # 블록 개수와 블록 중복 체크
        # given
        block_overlap_set = set()
        # when
        for transporter in MyTestCase.best_individual:
            process = transporter.works

            for block in process:
                block_overlap_set.add(block)
        # then
        print(len(block_overlap_set))
        self.assertEqual(len(block_overlap_set), config_dict['BLOCKS'])

    def test_결과_데이터_중량_무결성(self):
        # given
        result_individual = MyTestCase.best_individual
        # when
        for transporter in result_individual:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                self.assertEqual(transporter.available_weight, transporter.works[0].weight)


if __name__ == '__main__':
    unittest.main()
