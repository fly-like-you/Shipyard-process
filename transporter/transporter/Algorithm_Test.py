import unittest
from GA import *
import sys


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


    def test_data_list(self): # 데이터가 끝나기
        pop = generate_population(1)

        for i in range(10):
            print(pop[0][i])

    def test_data_integrity(self):
        pop = generate_population_will_delete(1)
        for i in range(10):
            print(pop[0][i])


if __name__ == '__main__':
    unittest.main()
