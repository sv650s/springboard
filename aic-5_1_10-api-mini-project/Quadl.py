import requests
from pprint import pformat
import logging
import argparse


logger = logging.getLogger(__name__)


class Quadl:

    api_key = None
    response = None
    start_date = None
    end_date = None
    database_code = None
    ticker_code = None
    order = None
    format = None
    data = None
    dataset_data = None
    data = None
    column_names = None

    def __init__(self,
                 api_key: str = None,
                 start_date: str = None,
                 end_date: str = None,
                 database_code: str = 'FSE',
                 ticker_code: str = 'AFX_X',
                 order: str = 'asc',
                 format: str = 'json'):
        self.api_key = api_key
        self.start_date = start_date
        self.end_date = end_date
        self.database_code = database_code
        self.ticker_code = ticker_code
        self.order = order
        self.format = format

        # TODO: figure out how to do this better so we don't have to make the call during unit tests
        self.data, self.column_names = self.__get_dataset()

    def __get_dataset(self):
        """
        Go out and gets the data based on URL passed
        """
        url = f"https://www.quandl.com/api/v3/datasets/{self.database_code}/{self.ticker_code}/" \
            f"data.{self.format}?api_key={self.api_key}&start_date={self.start_date}&" \
            f"end_date={self.end_date}&order={self.order}"
        logger.debug(url)

        self.response = requests.get(url)
        json_response = self.response.json()
        logger.debug(json_response)

        # check to make sure the response looks right
        assert json_response != None
        assert 'dataset_data' in json_response

        dataset_data = json_response['dataset_data']
        return (dataset_data['data'], dataset_data['column_names'])

    def sort_data(self, data: list, index: int) -> list:
        """
        Sorts the data array by index passed in

        Returns a copy of the list sorted
        """
        return sorted(data, key=lambda a: a[index])

    def summary(self):
        """
        Inspects the response data from Quadl API call
        """
        if self.data != None and self.column_names != None:
            print('Summary of Data:')
            print(f'\tstart date: {self.start_date}')
            print(f'\tend date: {self.end_date}')
            print(f'\tcolumn names: {self.column_names}')
            print(f'\tdata entries: {len(self.data)}')
        else:
            print('Unable to get data')

    def calculate_stats(self) -> dict:
        """
        Calculate what the highest and lowest opening prices were for the stock in this period.
        What was the largest change in any one day (based on High and Low price)?
        What was the largest change between any two days (based on Closing Price)?
        What was the average daily trading volume during this year?
        What was the median trading volume during this year. (Note: you may need to implement your own function for calculating the median.)

        Return:
        Dictionary with the following keys:
        min_open_price, max_open_price, max_two_day_change, average_trading_volume, 
        median_trading_volume
        """
        if self.data == None:
            return None

        return_dict = {}

        min_open_price = 0.0
        max_open_price = 0.0
        # Daily high - low
        max_daily_change = 0.0
        # closing today - closing yesterday
        max_two_day_change = 0.0
        # sum of all volume
        total_volume = 0.0

        date_index = self.column_names.index('Date')
        open_index = self.column_names.index('Open')
        high_index = self.column_names.index('High')
        low_index = self.column_names.index('Low')
        volume_index = self.column_names.index('Traded Volume')
        close_index = self.column_names.index('Close')

        # general counter
        count = 1
        # only increment this if we have a volume for the day
        volume_count = 0
        previous_closing_price = 0.0
        # Calculate most stats at once to keep it mostly O(n)
        for entry in self.data:
            # calculate min/max open price
            current_open_price = entry[open_index]
            logger.debug(
                f'date: {entry[date_index]} current_open_price: {current_open_price} current_open_price type: {type(current_open_price)}')
            if current_open_price != None:
                if min_open_price == 0 or current_open_price < min_open_price:
                    min_open_price = current_open_price
                if max_open_price < current_open_price:
                    max_open_price = current_open_price

            # calculate largest change
            current_high = entry[high_index]
            current_low = entry[low_index]
            if current_high != None and current_low != None:
                current_change = current_high - current_low
                if current_change > max_daily_change:
                    max_daily_change = current_change

            # largest change between 2 days based on closing price
            current_closing_price = entry[close_index]
            if count > 1:
                closing_diff = current_closing_price - previous_closing_price
                if closing_diff > max_two_day_change:
                    max_two_day_change = closing_diff
            previous_closing_price = current_closing_price

            # total volume for the year
            volume = entry[volume_index]
            if volume != None:
                total_volume += volume
                volume_count += 1

            count += 1

        return_dict['min_open_price'] = min_open_price
        return_dict['max_open_price'] = max_open_price
        return_dict['max_daily_change'] = round(max_daily_change, 2)
        return_dict['max_two_day_change'] = round(max_two_day_change, 2)
        # calculate average volume
        if volume_count > 1:
            return_dict['average_trading_volume'] = round(
                total_volume / (volume_count), 2)
        else:
            return_dict['average_trading_volume'] = 0.0

        return_dict['median_volume'] = self.calculate_median(
            self.data, volume_index)

        return return_dict

    def calculate_median(self, data_list: list, index: int) -> float:
        """
        given a 2D list and and index of column, calculate median of that column
        """
        # copy the list then calculate median trading volume
        data_length = len(data_list)
        sorted_data = self.sort_data(data_list, index)
        median = 0.0
        median_index = data_length // 2
        if data_length == 1:
            median = sorted_data[0][index]
        elif data_length % 2 > 0:
            median = sorted_data[median_index][index]
        else:
            """
            if list is even, we average the middle two numbers
            ie, if list length is 6, we take number at index 2 and 3 and average them
            """
            median = (sorted_data[median_index][index] +
                      sorted_data[median_index - 1][index]) / 2

        return round(median, 2)


if __name__ == '__main__':
    """
    Testing call to run this as a standalone program

    To specify log level use --log=<log level>
    """
    parser = argparse.ArgumentParser(description='Utility for quadl API')
    parser.add_argument('--start_date', type=str,
                        help='Start date to pull data', dest='start_date')
    parser.add_argument('--end_date', type=str,
                        help='End date to pull data', dest='end_date')
    parser.add_argument('--key', type=str,
                        help='set API key for quadl', dest='key')
    parser.add_argument('--log', type=str, default='INFO',
                        help='set log level for %(prog)s', dest='loglevel')
    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper())
    LOGGING_FORMAT = '%(asctime)-15s %(levelname)-10s - %(name)-20s.%(funcName)-15s (%(lineno)d) - %(message)s'
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    start_date = args.start_date
    end_date = args.end_date
    key = args.key
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    logger.debug(f"key {key}")

    # quadl = Quadl(start_date = '2017-01-01', end_date = '2017-12-31')
    quadl = Quadl(api_key = key, start_date = start_date, end_date = end_date)
    quadl.summary()

    stats = quadl.calculate_stats()
    print(f'min open: {stats["min_open_price"]}')
    print(f'max open: {stats["max_open_price"]}')
    print(f'max daily change: {stats["max_daily_change"]}')
    print(f'max 2 day change: {stats["max_two_day_change"]}')
    print(f'average trading volume: {stats["average_trading_volume"]}')
    print(f'median volume: {stats["median_volume"]}')
