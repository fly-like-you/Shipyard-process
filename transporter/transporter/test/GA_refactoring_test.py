import os
import unittest
from transporter.transporter.Configuration import Configuration
from transporter.transporter.GA_refactoring import GA
from transporter.transporter.create_data.FileManager import FileManager
# 박준호가 작성한 GA_refactoring 파일의 코드를 테스트하는 코드입니다.

class MyTestCase(unittest.TestCase):
    file_manager = FileManager()

    block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'map.xlsx')
    transporter_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'transporter.csv')

    config = Configuration(transporter_path, block_path)

    const_dict = config.get_GA_config()
    genetic_algorithm = GA(config.transporter_container, config.block_container, const_dict)
    ga_inititial_population = genetic_algorithm.generate_population(const_dict['POPULATION_SIZE'], config.transporter_container, config.block_container)
    ga_result = genetic_algorithm.run_GA()

    def test_generate_population(self): # 블록 개수와 블록 중복 체크
        # given
        block_overlap_set = set()
        # when
        for transporter_list in MyTestCase.ga_inititial_population:
            for transporter in transporter_list:
                process = transporter.works

                for block in process:
                    block_overlap_set.add(block)
        # then
        print(len(block_overlap_set))
        self.assertEqual(len(block_overlap_set), MyTestCase.const_dict['BLOCKS'])



    def test_결과_데이터_중량_무결성(self):
        # given
        result_individual = MyTestCase.ga_result
        # when
        for transporter in result_individual:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                self.assertEqual(transporter.available_weight, transporter.works[0].weight)


if __name__ == '__main__':
    unittest.main()
