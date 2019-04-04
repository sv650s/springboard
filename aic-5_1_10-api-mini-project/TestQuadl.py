import unittest
from unittest.mock import MagicMock
import logging
from Quadl import Quadl
from pprint import pformat

logger = logging.getLogger(__name__)


class TestQuadl(unittest.TestCase):

    def test_sort_data(self):
        """
        Test to make sure we are sorting the data array properly
        """
        # json = "{'dataset_data': {'limit': None, 'transform': None, 'column_index': None, 'column_names': ['Date', 'Open', 'High', 'Low', 'Close', 'Change', 'Traded Volume', 'Turnover', 'Last Price of the Day', 'Daily Traded Units', 'Daily Turnover'], 'start_date': '2017-01-01', 'end_date': '2017-01-04', 'frequency': 'daily', 'data': [['2017-01-02', 34.99, 35.94, 34.99, 35.8, None, 44700.0, 1590561.0, None, None, None], ['2017-01-03', 35.9, 35.93, 35.34, 35.48, None, 70618.0, 2515473.0, None, None, None], ['2017-01-04', 35.48, 35.51, 34.75, 35.19, None, 54408.0, 1906810.0, None, None, None]], 'collapse': None, 'order': 'asc'}}"
        unsorted_list = [['2017-01-02', 34.99, 35.94, 34.99, 35.8, None, 44700.0, 1590561.0, None, None, None],
                         ['2017-01-03', 35.9, 35.93, 35.34, 35.48, None,
                             70618.0, 2515473.0, None, None, None],
                         ['2017-01-04', 35.48, 35.51, 34.75, 35.19, None, 54408.0, 1906810.0, None, None, None]]
        # unsorted_list = list(list_string)
        assert len(
            unsorted_list) == 3, f"list should be length of 3 but found {len(list)}"
        quadl = Quadl(start_date='2017-01-01', end_date='2017-01-04')
        # quadl.__get_dataset = MagicMock(return_value=json)
        # quadl.__get_dataset()

        # sort by index 3 should give us 04, 02, 03
        sorted_list = quadl.sort_data(unsorted_list, 3)
        assert sorted_list[0][
            0] == '2017-01-04', f'first should be 04. found {sorted_list[0][0]}'
        assert sorted_list[1][
            0] == '2017-01-02', f'first should be 02. found {sorted_list[1][0]}'
        assert sorted_list[2][
            0] == '2017-01-03', f'first should be 03. found {sorted_list[2][0]}'


if __name__ == '__main__':
    unittest.main()
