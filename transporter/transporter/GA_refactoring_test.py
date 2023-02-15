import unittest
from GA_refactoring import *
from create_data.block import blocks, BLOCKS  # 블록, 트랜스포터 정보 가져오기
from create_data.transporter import transporters
# 박준호가 작성한 GA_refactoring 파일의 코드를 테스트하는 코드입니다.

class MyTestCase(unittest.TestCase):
    population = generate_population(100, transporters, blocks)

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

        fitness_values = [fitness(p) for p in MyTestCase.population]
        fitness_values.sort()
        print(fitness_values)

    def test_selection(self):
        pass



if __name__ == '__main__':
    unittest.main()
