import unittest
from GA import *
import sys


class MyTestCase(unittest.TestCase):
    def test_초기_데이터_갯수(self): # 데이터가 끝나기
        # given
        count = 0
        population = generate_population(1)
        transporter_list = population[0]

        # when
        for transporter in transporter_list:
            process = transporter.works
            if process:
                count += len(process)

        # then
        self.assertEqual(count, 100)


    def test_데이터_중량_무결성(self):
        # given
        population = generate_population(1)
        transporter_list = population[0]

        # when
        for transporter in transporter_list:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                self.assertEqual(transporter.available_weight, transporter.works[0].weight)
        # then

    def test_데이터_시간_무결성(self):
        # given
        population = generate_population(1)
        transporter_list = population[0]

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
    def test_결과_데이터(self): # 결과 데이터의 개수가 맞는가?
        # given
        transporter_list, a = run_ga()

        li = []
        for i in transporter_list:
            if i.works:
                for j in i.works:
                    li.append(j.no)

        li.sort()
        print(li)
        # when

        # then
    def test_결과_데이터_중량_무결성(self):
        # given
        transporter_list, a = run_ga()

        # when
        for transporter in transporter_list:
            if any(work.weight > transporter.available_weight for work in transporter.works):
                self.assertEqual(transporter.available_weight, transporter.works[0].weight)

if __name__ == '__main__':
    unittest.main()
