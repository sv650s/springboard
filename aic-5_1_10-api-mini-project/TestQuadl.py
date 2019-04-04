import unittest
from unittest.mock import MagicMock
import logging
from Quadl import Quadl
from pprint import pformat
import pandas as pd

logger = logging.getLogger(__name__)


class TestQuadl(unittest.TestCase):

    def setUp(self):
        self.quadl = Quadl(start_date='2017-01-01', end_date='2017-01-04')
        # make a copy of this list
        self.quadl.data = [['2017-01-02', 34.99, 35.94, 34.99, 35.8, None, 44700.0, 1590561.0, None, None, None],
                           ['2017-01-03', 35.9, 35.93, 35.34, 35.48, None,
                            70618.0, 2515473.0, None, None, None],
                           ['2017-01-04', 35.48, 35.51, 34.75, 35.19,
                            None, 54408.0, 1906810.0, None, None, None],
                           ['2017-01-05', 35.48, 50.00, 50.00, 35.19,
                            None, 54408.0, 1906810.0, None, None, None],
                           ]
        self.quadl.column_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Change', 'Traded Volume',
                                   'Turnover', 'Last Price of the Day', 'Daily Traded Units', 'Daily Turnover']
        # 1/2 to 2/1
        # [['2017-01-02', 34.99, 35.94, 34.99, 35.8, None, 44700.0, 1590561.0, None, None, None], ['2017-01-03', 35.9, 35.93, 35.34, 35.48, None, 70618.0, 2515473.0, None, None, None], ['2017-01-04', 35.48, 35.51, 34.75, 35.19, None, 54408.0, 1906810.0, None, None, None], ['2017-01-05', 35.02, 35.2, 34.73, 35.06, None, 48412.0, 1692326.0, None, None, None], ['2017-01-06', 34.91, 35.21, 34.91, 35.04, None, 27507.0, 964046.0, None, None, None], ['2017-01-09', 35.29, 35.35, 34.43, 34.67, None, 62225.0, 2157182.0, None, None, None], ['2017-01-10', 34.8, 34.98, 34.46, 34.91, None, 43976.0, 1528055.0, None, None, None], ['2017-01-11', 34.95, 36.0, 34.84, 35.42, None, 123530.0, 4369079.0, None, None, None], ['2017-01-12', 35.38, 35.38, 34.31, 34.9, None, 163860.0, 5703427.0, None, None, None], ['2017-01-13', 34.98, 34.98, 34.6, 34.85, None, 59367.0, 2065534.0, None, None, None], ['2017-01-16', 34.85, 35.24, 34.56, 35.07, None, 47879.0, 1678679.0, None, None, None], ['2017-01-17', 35.06, 35.19, 34.79, 34.99, None, 39195.0, 1369857.0, None, None, None], ['2017-01-18', 35.04, 35.51, 34.8, 34.9, None, 65931.0, 2311608.0, None, None, None], ['2017-01-19', 35.04, 35.04, 34.42, 34.5, None, 73105.0, 2526731.0, None, None, None], ['2017-01-20', 34.54, 34.59, 34.05, 34.17, None, 80246.0, 2743474.0, None, None, None], ['2017-01-23', 34.04, 34.12, 33.62, 34.06, None, 55333.0, 1877957.0, None, None, None], ['2017-01-24', 34.0, 34.35, 33.85, 34.22, None, 48797.0, 1666086.0, None, None, None], ['2017-01-25', 34.42, 34.86, 34.03, 34.83, None, 56240.0, 1947147.0, None, None, None], ['2017-01-26', 35.07, 35.58, 34.8, 34.89, None, 64103.0, 2249375.0, None, None, None], ['2017-01-27', 34.83, 35.43, 34.81, 35.3, None, 69657.0, 2444913.0, None, None, None], ['2017-01-30', 35.38, 35.59, 34.95, 35.15, None, 69603.0, 2457762.0, None, None, None], ['2017-01-31', 35.24, 35.24, 34.56, 34.56, None, 63371.0, 2199583.0, None, None, None], ['2017-02-01', 34.75, 36.0, 34.75, 35.94, None, 85137.0, 3038172.0, None, None, None]]

    def test_sort_data(self):
        """
        Test to make sure we are sorting the data array properly
        """
        unsorted_list = [['2017-01-02', 34.99, 35.94, 34.99, 35.8, None, 44700.0, 1590561.0, None, None, None],
                         ['2017-01-03', 35.9, 35.93, 35.34, 35.48, None,
                          70618.0, 2515473.0, None, None, None],
                         ['2017-01-04', 35.48, 35.51, 34.75, 35.19,
                          None, 54408.0, 1906810.0, None, None, None],
                         ['2017-01-05', 35.48, 50.00, 50.00, 35.19,
                          None, 54408.0, 1906810.0, None, None, None],
                         ]
        assert len(
            unsorted_list) == 4, f"list should be length of 4 but found {len(unsorted_list)}"

        # sort by index 3 should give us 04, 02, 03
        sorted_list = self.quadl.sort_data(unsorted_list, 3)
        assert sorted_list[0][
            0] == '2017-01-04', f'first should be 04. found {sorted_list[0][0]}'
        assert sorted_list[1][
            0] == '2017-01-02', f'second should be 02. found {sorted_list[1][0]}'
        assert sorted_list[2][
            0] == '2017-01-03', f'third should be 03. found {sorted_list[2][0]}'
        assert sorted_list[3][
            0] == '2017-01-05', f'forth should be 05. found {sorted_list[3][0]}'

    def test_calculate_median(self):
        """
        Test calculate median
        """
        # if odd length, then middle number is returned
        list1 = [[1], [2], [3]]
        median1 = self.quadl.calculate_median(list1, 0)
        assert median1 == 2, f'median should be 2 but got {median1}'

        # if even length, then average of middle 2 numbers is returned
        list2 = [[1], [2], [3], [4]]
        median2 = self.quadl.calculate_median(list2, 0)
        assert median2 == 2.50, f'median should be 2.50 but got {median2}'

    def test_calculate_stats(self):
        """
        Test stats
        """
        stats = self.quadl.calculate_stats()


if __name__ == '__main__':
    unittest.main()
