#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Rohit Gupta'

"""
Cryptocurrency price History from coinmarketcap.com
"""

from __future__ import print_function

__all__ = ['CmcScraper']

import os
import csv
from .utils import download_coin_data, extract_data, InvalidParameters


class CmcScraper(object):
    """
    Scrape cryptocurrency historical market price data from coinmarketcap.com

    """

    def __init__(self, coin_code, start_date=None, end_date=None, all_time=False):
        """
        :param coin_code: coin code of cryptocurrency e.g. btc
        :param start_date: date since when to scrape data (in the format of dd-mm-yyyy)
        :param end_date: date to which scrape the data (in the format of dd-mm-yyyy)
        :param all_time: 'True' if need data of all time for respective cryptocurrency

        """

        self.coin_code = coin_code
        self.start_date = start_date
        self.end_date = end_date
        self.all_time = bool(all_time)
        self.headers = []
        self.rows = []

        # enable all_time download if start_time or end_time is not given
        if not (self.start_date and self.end_date):
            self.all_time = True

        if not (self.all_time or (self.start_date and self.end_date)):
            raise InvalidParameters("'start_date' or 'end_date' cannot be empty if 'all_time' flag is False")

    def __repr__(self):
        return '<CmcScraper coin_code:{}, start_date:{}, end_date:{}, all_time:{}>'.format(self.coin_code,
                                                                                           self.start_date,
                                                                                           self.end_date,
                                                                                           self.all_time)

    def _download_data(self, **kwargs):
        """
        This method downloads the data.
        :param forced: (optional) if ``True``, data will be re-downloaded.
        :return:
        """

        forced = kwargs.get('forced')

        if self.headers and self.rows and not forced:
            return

        if self.all_time:
            self.start_date, self.end_date = None, None

        table = download_coin_data(self.coin_code, self.start_date, self.end_date)

        # self.headers, self.rows, self.start_date, self.end_date = extract_data(table)
        self.end_date, self.start_date, self.headers, self.rows = extract_data(table)

    def get_data(self, verbose=False, **kwargs):

        """
        This method fetches downloaded the data.
        :param verbose: (optional) Flag to enable verbose.
        :param kwargs: Optional arguments that data downloader takes.
        :return:
        """

        self._download_data(**kwargs)

        if verbose:
            print(*self.headers, sep=', ')

            for row in self.rows:
                print(*row, sep=', ')
        else:
            return self.headers, self.rows

    def get_dataframe(self, **kwargs):
        """
        This gives scraped data as DataFrame.
        :param kwargs: Optional arguments that data downloader takes.
        :return: DataFrame of the downloaded data.
        """

        try:
            import pandas as pd
        except ImportError:
            pd = None

        if pd is None:
            raise NotImplementedError(
                "DataFrame Format requires 'pandas' to be installed."
                "Try : pip install pandas")

        self._download_data(**kwargs)

        dataframe = pd.DataFrame(data=self.rows, columns=self.headers)

        # convert 'Date' column to datetime type
        dataframe['Date'] = pd.to_datetime(dataframe['Date'], dayfirst=True)
        return dataframe

    def export_csv(self, csv_name=None, csv_path=None, **kwargs):
        """
        This exports scraped data into a csv.
        :param csv_name: (optional) name of csv file.
        :param csv_path: (optional) path to where export csv file.
        :param kwargs: Optional arguments that data downloader takes.
        :return:
        """

        self._download_data(**kwargs)

        if csv_path is None:
            # Export in current directory if path not specified
            csv_path = os.getcwd()

        if csv_name is None:
            # Make name fo file in format of {coin_code}_{start_date}_{end_date}.csv
            csv_name = '{0}_{1}_{2}.csv'.format(self.coin_code, self.start_date, self.end_date)

        if not csv_name.endswith('.csv'):
            csv_name += '.csv'

        _csv = '{0}/{1}'.format(csv_path, csv_name)

        try:
            with open(_csv, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(self.headers)
                for data in self.rows:
                    writer.writerow(data)
        except IOError as err:
            errno, strerror = err.args
            print('I/O error({0}): {1}'.format(errno, strerror))
