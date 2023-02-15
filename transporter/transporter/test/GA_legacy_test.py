import unittest
from GA_legacy import *
import sys
from GA_refactoring import fitness

class legacy_ga_test(unittest.TestCase):
    initial_individual = generate_population(1)
    result_individual, a = run_ga()

    def test_초기_데이터_갯수(self): # 데이터가 끝나기
        # given
        count = 0
        result_individual = legacy_ga_test.population[0]

        # when
        for transporter in result_individual:
            process = transporter.works
            if process:
                count += len(process)

        # then
        self.assertEqual(count, 100)


    def test_데이터_중량_무결성(self):
        # given
        transporter_list = legacy_ga_test.population[0]


        # when
        for transporter in transporter_list:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                self.assertEqual(transporter.available_weight, transporter.works[0].weight)
        # then

    def test_데이터_시간_무결성(self):
        # given
        transporter_list = legacy_ga_test.population[0]

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

    def test_내가_짠_코드와비교(self):
        transporter_list = legacy_ga_test.result_individual

        fitness_values = fitness(transporter_list)
        print(fitness_values)



if __name__ == '__main__':
    unittest.main()
