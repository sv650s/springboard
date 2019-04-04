import unittest
from unittest.mock import MagicMock
import logging
from Quadl import Quadl
from pprint import pformat
import pandas as pd

logger = logging.getLogger(__name__)


class TestQuadl(unittest.TestCase):

    def setUp(self):
        self.df = pd.read_csv('data_year.csv')

        self.quadl = Quadl(start_date='2017-01-01', end_date='2017-01-04')
        # make a copy of this list
        self.quadl.data = self.df.values.tolist()
        self.quadl.column_names = self.df.columns.values.T.tolist()

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
        # prepare datafraem
        self.df['daily_change'] = self.df.High - self.df.Low

        stats = self.quadl.calculate_stats()

        min_open_price = stats['min_open_price']
        assert stats['min_open_price'] == self.df.Open.min(), \
            f"min open price should be {self.df.Open.min()} but got {min_open_price}"
        max_open_price = stats['max_open_price']
        assert stats['max_open_price'] == self.df.Open.max(), \
            f"max open price should be {self.df.Open.max()} but got {max_open_price}"
        max_daily_change = stats['max_daily_change']
        assert max_daily_change == round(self.df.daily_change.max(), 2), \
            f"max daily_change should be {round(self.df.daily_change.max(), 2)} but got {max_daily_change}"
        average_trading_volume = stats['average_trading_volume']
        assert average_trading_volume == round(self.df['Traded Volume'].mean(), 2), \
            f"average traded volumen should be {round(self.df['Traded Volume'].mean(), 2)} but got {average_trading_volume}"
        
        # TODO: check max 2 day change


if __name__ == '__main__':
    unittest.main()
