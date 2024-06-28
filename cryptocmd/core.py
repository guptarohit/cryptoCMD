#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Rohit Gupta'

"""
Cryptocurrency price History from coinmarketcap.com
"""

from __future__ import print_function

__all__ = ["CmcScraper"]

import os
import csv
import tablib
import warnings
from datetime import datetime
from .utils import download_coin_data, InvalidParameters


class CmcScraper(object):
    """
    Scrape cryptocurrency historical market price data from coinmarketcap.com

    """

    def __init__(
        self,
        coin_code=None,
        start_date=None,
        end_date=None,
        all_time=False,
        order_ascending=False,
        fiat="USD",
        coin_name=None,
        id_number=None,
    ):
        """
        Initialize the CmcScraper object.

        Args:
            coin_code (str): Coin code of the cryptocurrency (e.g. btc).
                Will be ignored if using id_number.
            start_date (str): Date since when to scrape data (in the format of dd-mm-yyyy).
            end_date (str): Date to which scrape the data (in the format of dd-mm-yyyy).
            all_time (bool): If True, download data for all time for the respective cryptocurrency.
            order_ascending (bool): If True, data is ordered by 'Date' in ascending order (oldest first).
            fiat (str): Fiat code (e.g. USD, EUR).
            coin_name (str): Coin name in case of multiple coins with the same code
                (e.g. sol -> solana, solcoin).
            id_number (int): ID number for the cryptocurrency on the CoinMarketCap website.
                Overrides coin_code and coin_name when provided.
        """

        # Initialize attributes
        self.coin_code = coin_code
        self.start_date = start_date
        self.end_date = end_date
        self.all_time = bool(all_time)
        self.order_ascending = order_ascending
        self.fiat = fiat
        self.coin_name = coin_name
        self.headers = [
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Market Cap",
            "Time Open",
            "Time High",
            "Time Low",
            "Time Close",
        ]
        self.rows = []
        self.id_number = id_number

        # Enable all_time download if start_time or end_time is not given
        if not (self.start_date and self.end_date):
            self.all_time = True

        # Raise error if neither all_time nor start_date and end_date are given
        if not (self.all_time or (self.start_date and self.end_date)):
            raise InvalidParameters(
                "'start_date' or 'end_date' cannot be empty if 'all_time' flag is False"
            )

    def __repr__(self):
        """
        Return string representation of the object.
        
        Returns:
            str: String representation of the object.
        """
        
        # Format the string with the object's attributes
        return (
            "<CmcScraper "
            "coin_code:{}, "
            "start_date:{}, "
            "end_date:{}, "
            "all_time:{}>".format(
                self.coin_code, self.start_date, self.end_date, self.all_time
            )
        )

    def _download_data(self, **kwargs):
        """
        This method downloads the data.
        :param forced: (optional) if ``True``, data will be re-downloaded.
        :return:
        """

        forced = kwargs.get("forced")

        if self.rows and not forced:
            return

        if self.all_time:
            self.start_date, self.end_date = None, None

        coin_data = download_coin_data(
            self.coin_code,
            self.start_date,
            self.end_date,
            self.fiat,
            self.coin_name,
            self.id_number,
        )

        for _row in coin_data["data"]["quotes"]:
            _row_quote = list(_row["quote"].values())[0]
            date = datetime.strptime(
                _row_quote["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ).strftime("%d-%m-%Y")

            row = [
                date,
                _row_quote["open"],
                _row_quote["high"],
                _row_quote["low"],
                _row_quote["close"],
                _row_quote["volume"],
                _row_quote["market_cap"],
                _row["time_open"],
                _row["time_high"],
                _row["time_low"],
                _row["time_close"],
            ]

            self.rows.insert(0, row)

        self.end_date, self.start_date = self.rows[0][0], self.rows[-1][0]

        if self.order_ascending:
            self.rows.sort(key=lambda x: datetime.strptime(x[0], "%d-%m-%Y"))

    def get_data(self, format="", verbose=False, **kwargs):
        """
        This method returns the downloaded data in specified format.

        :param format: Extension name of data format. Available: json, xls, yaml, csv, dbf, tsv, html, latex, xlsx, ods.
        :param verbose: (optional) Flag to enable verbose only.
        :param kwargs: Optional arguments that data downloader takes.
        :return: Data in specified format, or if format is not specified, returns headers and rows.
        """

        # Download the data
        self._download_data(**kwargs)

        # If verbose flag is set, print the data
        if verbose:
            # Print the headers
            print(*self.headers, sep=", ")

            # Print each row of data
            for row in self.rows:
                print(*row, sep=", ")
        # If format is specified, export the data in that format
        elif format:
            # Create a new tablib Dataset and add headers
            data = tablib.Dataset()
            data.headers = self.headers

            # Add each row of data to the Dataset
            for row in self.rows:
                data.append(row)

            # Export the Dataset in the specified format and return it
            return data.export(format)
        # If no format is specified, return the headers and rows
        else:
            return self.headers, self.rows

    def get_dataframe(self, date_as_index=False, **kwargs):
        """
        This gives scraped data as DataFrame.
        :param date_as_index: make 'Date' as index and remove 'Date' column.
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
                "Try : pip install pandas"
            )

        self._download_data(**kwargs)

        dataframe = pd.DataFrame(data=self.rows, columns=self.headers)

        # convert 'Date' column to datetime type
        dataframe["Date"] = pd.to_datetime(
            dataframe["Date"], format="%d-%m-%Y", dayfirst=True
        )

        if date_as_index:
            # set 'Date' column as index and drop the the 'Date' column.
            dataframe.set_index("Date", inplace=True)

        return dataframe

    def export_csv(self, csv_name=None, csv_path=None, **kwargs):
        """
        This exports scraped data into a csv.
        :param csv_name: (optional) name of csv file.
        :param csv_path: (optional) path to where export csv file.
        :param kwargs: Optional arguments that data downloader takes.
        :return:
        """
        warnings.warn(
            "export_csv will be deprecated; Use 'export' method instead, e.g. export('csv')",
            PendingDeprecationWarning,
            stacklevel=2,
        )

        self._download_data(**kwargs)

        if csv_path is None:
            # Export in current directory if path not specified
            csv_path = os.getcwd()

        if csv_name is None:
            # Make name fo file in format of {coin_code}_{fiat}_{start_date}_{end_date}.csv
            csv_name = "{0}_{1}_{2}_{3}.csv".format(
                self.coin_code, self.fiat, self.start_date, self.end_date
            )

        if not csv_name.endswith(".csv"):
            csv_name += ".csv"

        _csv = "{0}/{1}".format(csv_path, csv_name)

        try:
            with open(_csv, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=",", quoting=csv.QUOTE_NONNUMERIC
                )
                writer.writerow(self.headers)
                for data in self.rows:
                    writer.writerow(data)
        except IOError as err:
            errno, strerror = err.args
            print("I/O error({0}): {1}".format(errno, strerror))

    def export(self, format, name=None, path=None, **kwargs):
        """
        Exports the data to specified file format

        :param format: extension name of file format. Available: json, xls, yaml, csv, dbf, tsv, html, latex, xlsx, ods
        :param name: (optional) name of file.
        :param path: (optional) output file path.
        :param kwargs: Optional arguments that data downloader takes.
        :return:
        """

        # Get the data in the specified format
        data = self.get_data(format, **kwargs)

        if path is None:
            # Export in current directory if path not specified
            path = os.getcwd()

        if name is None:
            # Make name of file in format: {coin_code}_{fiat}_{start_date}_{end_date}.csv
            name = "{0}_{1}-{2}_{3}".format(
                self.coin_code, self.fiat, self.start_date, self.end_date
            )

        if not name.endswith(".{}".format(format)):
            # Add the file extension if not provided
            name += ".{}".format(format)

        _file = "{0}/{1}".format(path, name)

        try:
            # Write the data to the file
            with open(_file, "wb") as f:
                if isinstance(data, str):
                    # If data is a string, encode it to bytes
                    f.write(data.encode("utf-8"))
                else:
                    # If data is not a string, simply write it to the file
                    f.write(data)
        except IOError as err:
            errno, strerror = err.args
            print("I/O error({0}): {1}".format(errno, strerror))
        except Exception as err:
            # Catch any other exception and print the format and error message
            print("format: {0}, Error: {1}".format(format, err))
