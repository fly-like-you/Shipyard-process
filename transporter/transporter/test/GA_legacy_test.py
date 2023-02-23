import unittest
from transporter.transporter.GA_legacy.GA_legacy import *
from transporter.transporter.create_data.FileManager import FileManager


class legacy_ga_test(unittest.TestCase):
    file_manager = FileManager()
    transporter_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'transporter.csv')
    block_path = os.path.join(os.getcwd(), '..', 'create_data', 'data', 'blocks.csv')
    
    block_container = file_manager.load_block_data(block_path, 100)
    transporter_container = file_manager.load_transporters(transporter_path)

    result_individual = run_ga(transporter_container, block_container)
    result_individual = result_individual['best_individual']

    def test_초기_데이터_갯수(self):  # 데이터가 끝나기
        # given
        count = 0
        result_individual = legacy_ga_test.result_individual

        # when
        for transporter in result_individual:
            process = transporter.works
            if process:
                count += len(process)

        # then
        self.assertEqual(count, 100)

    def test_데이터_중량_무결성(self):
        # given
        transporter_list = legacy_ga_test.result_individual

        # when
        for transporter in transporter_list:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                self.assertEqual(transporter.available_weight, transporter.works[0].weight)
        # then

    def test_데이터_시간_무결성(self):
        # given
        transporter_list = legacy_ga_test.result_individual

        optimization_count = 0
        work = 0
        optimization_time = 0
        for i in transporter_list:
            if i.works:
                optimization_count += 1
                work += len(i.works)
                optimization_time += evaluation(i)
        # when

        # then

    def test_결과_데이터_중량_무결성(self):
        # given
        transporter_list = legacy_ga_test.result_individual

        # when
        for transporter in transporter_list:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                self.assertEqual(transporter.available_weight, transporter.works[0].weight)


if __name__ == '__main__':
    unittest.main()
