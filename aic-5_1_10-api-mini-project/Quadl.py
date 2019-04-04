import requests
from pprint import pformat
import logging
import argparse


logger = logging.getLogger(__name__)


class Quadl:

    API_KEY = 'JUFS6eBwXFLthN3_ARFz'
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

    def __init__(self: "Quadl",
                 start_date: str = None,
                 end_date: str = None,
                 database_code: str = 'FSE',
                 ticker_code: str = 'AFX_X',
                 order: str = 'asc',
                 format: str = 'json'):
        self.start_date = start_date
        self.end_date = end_date
        self.database_code = database_code
        self.ticker_code = ticker_code
        self.order = order
        self.format = format

    def __get_dataset(self):
        """
        Go out and gets the data based on URL passed
        """
        url = f"https://www.quandl.com/api/v3/datasets/{self.database_code}/{self.ticker_code}/" \
            f"data.{self.format}?api_key={self.API_KEY}&start_date={self.start_date}&" \
            f"end_date={self.end_date}&order={self.order}"
        logger.debug(url)

        json_response = requests.get(url).json()
        logger.debug(json_response)
        # check to make sure the response looks right
        assert json_response != None
        assert 'dataset_data' in json_response

        self.dataset_data = json_response['dataset_data']
        self.data = self.dataset_data['data']
        self.column_names = self.dataset_data['column_names']

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
        if (self.dataset_data == None):
            self.__get_dataset()

        if (self.dataset_data != None):
            print('Summary of Data:')
            print(f'\tstart date: {self.dataset_data["start_date"]}')
            print(f'\tend date: {self.dataset_data["end_date"]}')
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
        if (self.dataset_data == None):
            self.__get_dataset()

        return_dict = {}

        min_open_price = 0.0
        max_open_price = 0.0
        # Daily high - low
        max_daily_change = 0.0
        # closing today - closing yesterday
        max_two_day_change = 0.0
        # sum of all volume
        total_volume = 0.0

        open_index = self.column_names.index('Open')
        high_index = self.column_names.index('High')
        low_index = self.column_names.index('Low')
        volume_index = self.column_names.index('Traded Volume')
        close_index = self.column_names.index('Close')

        # counter
        count = 1
        for entry in self.data:
            # calculate min/max open price
            current_open_price = entry[open_index]
            logger.debug(
                f'count: {count} current_open_price: {current_open_price} current_open_price type: {type(current_open_price)}')
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
            previous_closing_price = 0.0
            if count > 1:
                current_closing_price = entry[close_index]
                closing_diff = current_closing_price - previous_closing_price
                if closing_diff > max_two_day_change:
                    max_two_day_change = closing_diff
            else:
                previous_closing_price = entry[close_index]

            # total volume for the year
            volume = entry[volume_index]
            if volume != None:
                total_volume += volume

            count += 1

        # copy the list then calculate median trading volume
        data_length = len(self.data)
        sorted_data = self.sort_data(self.data, volume_index)
        median_volume = 0.0
        median_index = data_length // 2
        if data_length == 1:
            median_volume = sorted_data[0][volume_index]
        elif data_length % 2 > 0:
            median_volume = sorted_data[median_index][volume_index]
        else:
            median_volume = (sorted_data[median_index][volume_index] +
                             sorted_data[median_index - 1][volume_index]) / 2

        return_dict['min_open_price'] = min_open_price
        return_dict['max_open_price'] = max_open_price
        return_dict['max_daily_change'] = max_daily_change
        return_dict['max_two_day_change'] = max_two_day_change
        # calculate average volume
        return_dict['average_trading_volume'] = total_volume / (count - 1)
        return_dict['median_volume'] = median_volume

        return return_dict


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
    parser.add_argument('--log', type=str, default='INFO',
                        help='set log level for %(prog)s', dest='loglevel')
    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper())
    start_date = args.start_date
    end_date = args.end_date
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    LOGGING_FORMAT = '%(asctime)-15s %(levelname)-10s - %(name)-20s.%(funcName)-15s (%(lineno)d) - %(message)s'
    logging.basicConfig(format=LOGGING_FORMAT, level=numeric_level)

    # quadl = Quadl(start_date = '2017-01-01', end_date = '2017-12-31')
    quadl = Quadl(start_date=start_date, end_date=end_date)
    response = quadl.dataset_data
    logger.debug(pformat(response))
    quadl.summary()

    return_dict = quadl.calculate_stats()

    logger.info(f'min open: {return_dict["min_open_price"]}')
    logger.info(f'max open: {return_dict["max_open_price"]}')
    logger.info(f'max daily chnage: {return_dict["max_daily_change"]}')
    logger.info(f'max 2 day chnage: {return_dict["max_two_day_change"]}')
    logger.info(
        f'average trading volume: {return_dict["average_trading_volume"]}')
    logger.info(f'median volume: {return_dict["median_volume"]}')
