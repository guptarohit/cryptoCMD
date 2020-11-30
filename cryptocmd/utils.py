#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import datetime
from pyquery import PyQuery as pq
from requests import get


def get_url_data(url):
    """
    This method downloads the data of the web page.
    :param url: 'url' of the web page to download
    :return: response object of get request of the 'url'
    """

    try:
        response = get(url)
        return response
    except Exception as e:
        if hasattr(e, "message"):
            print("Error message (get_url_data) :", e.message)
        else:
            print("Error message (get_url_data) :", e)
        raise e


def get_coin_id(coin_code):
    """
    This method fetches the name(id) of currency from the given code
    :param coin_code: coin code of a cryptocurrency e.g. btc
    :return: coin-id for the a cryptocurrency on the coinmarketcap.com
    """

    try:
        url = "https://coinmarketcap.com/all/views/all/"

        html = get_url_data(url).text
        raw_data = pq(html)

        coin_code = coin_code.upper()
        data_table = raw_data("tbody")[0]

        for _row in data_table.findall("tr"):
            symbol = _row.findall("td")[2].text_content()
            coin_link = _row.findall("td")[1].find_class("cmc-link")[0]
            coin_id = coin_link.values()[0].split("/")[-2]
            if symbol == coin_code:
                return coin_id
        raise InvalidCoinCode("'{}' coin code is unavailable on coinmarketcap.com".format(coin_code))
    except Exception as e:
        raise e


def download_coin_data(coin_code, start_date, end_date):
    """
    Download HTML price history for the specified cryptocurrency and time range from CoinMarketCap.

    :param coin_code: coin code of a cryptocurrency e.g. btc
    :param start_date: date since when to scrape data (in the format of dd-mm-yyyy)
    :param end_date: date to which scrape the data (in the format of dd-mm-yyyy)
    :return: returns html of the webpage having historical data of cryptocurrency for certain duration
    """

    if start_date is None:
        # default start date on coinmarketcap.com
        start_date = "28-4-2013"

    if end_date is None:
        yesterday = datetime.date.today() - datetime.timedelta(1)
        end_date = yesterday.strftime("%d-%m-%Y")

    coin_id = get_coin_id(coin_code)

    # convert the dates to timestamp for the url
    start_date_timestamp = int(
        (
            datetime.datetime.strptime(start_date, "%d-%m-%Y")
            - datetime.timedelta(days=1)
        )
        .replace(tzinfo=datetime.timezone.utc)
        .timestamp()
    )

    end_date_timestamp = int(
        datetime.datetime.strptime(end_date, "%d-%m-%Y")
        .replace(tzinfo=datetime.timezone.utc)
        .timestamp()
    )

    api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert=USD&slug={}&time_end={}&time_start={}".format(
        coin_id, end_date_timestamp, start_date_timestamp
    )

    try:
        json_data = get_url_data(api_url).json()
        if json_data["status"]["error_code"] != 0:
            raise Exception(json_data["status"]["error_message"])
        return json_data
    except Exception as e:
        print(
            "Error fetching price data for {} for interval '{}' and '{}'",
            coin_code,
            start_date,
            end_date,
        )

        if hasattr(e, "message"):
            print("Error message (download_data) :", e.message)
        else:
            print("Error message (download_data) :", e)


def _replace(s, bad_chars):
    if sys.version_info > (3, 0):
        # For Python 3
        without_bad_chars = str.maketrans("", "", bad_chars)
        return s.translate(without_bad_chars)
    else:
        # For Python 2
        import string

        identity = string.maketrans("", "")
        return s.translate(identity, bad_chars)


class InvalidParameters(ValueError):
    """Passed parameters are invalid."""


class InvalidCoinCode(NotImplementedError):
    """This coin code is unavailable on 'coinmarketcap.com'"""
