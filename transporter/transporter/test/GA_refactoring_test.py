import unittest
from GA_refactoring import *
from create_data.Block import BLOCKS  # 블록, 트랜스포터 정보 가져오기
from transporter.transporter.create_data.FileManager import blocks
from create_data.Transporter import transporters
# 박준호가 작성한 GA_refactoring 파일의 코드를 테스트하는 코드입니다.

class MyTestCase(unittest.TestCase):
    population = generate_population(100, transporters, blocks)
    best_individual = run_GA()

    def test_generate_population(self): # 블록 개수와 블록 중복 체크
        # given
        block_overlap_set = set()

        # when
        for transporter_list in MyTestCase.population:
            for transporter in transporter_list:
                process = transporter.works

                for block in process:
                    block_overlap_set.add(block)

        # then
        self.assertEqual(len(block_overlap_set), BLOCKS)

    def test_fitness(self):
        # given
        pass


    def test_결과_데이터_중량_무결성(self):
        # given
        result_individual = MyTestCase.best_individual
        # when
        for transporter in result_individual:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                self.assertEqual(transporter.available_weight, transporter.works[0].weight)


if __name__ == '__main__':
    unittest.main()
