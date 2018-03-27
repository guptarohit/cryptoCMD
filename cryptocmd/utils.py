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
        if hasattr(e, 'message'):
            print('Error message (get_url_data) :', e.message)
        else:
            print('Error message (get_url_data) :', e)
        sys.exit(1)


def get_coin_id(coin_code):
    """
    This method fetches the name(id) of currency from the given code
    :param coin_code: coin code of a cryptocurrency e.g. btc
    :return: coin-id for the a cryptocurrency on the coinmarketcap.com
    """

    try:
        url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'

        json_resp = get_url_data(url).json()

        coin_code = coin_code.upper()

        for coin in json_resp:
            if coin['symbol'] == coin_code:
                return coin['id']
        raise InvalidCoinCode('This coin code is unavailable on "coinmarketcap.com"')
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
        start_date = '28-4-2013'

    if end_date is None:
        yesterday = datetime.date.today() - datetime.timedelta(1)
        end_date = yesterday.strftime('%d-%m-%Y')

    coin_id = get_coin_id(coin_code)

    # Format the dates as required for the url.
    start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y%m%d')
    end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y%m%d')

    url = 'https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}'.format(coin_id, start_date,
                                                                                               end_date)

    try:
        html = get_url_data(url).text
        return html
    except Exception as e:
        print("Error fetching price data for {} for interval '{}' and '{}'", coin_code, start_date, end_date)

        if hasattr(e, 'message'):
            print('Error message (download_data) :', e.message)
        else:
            print('Error message (download_data) :', e)


def _native_type(s):
    """
    Convert value in the string to its native (i.e. either int, float or str) type.
    :param s: string
    :return: value in native type
    """

    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def _replace(s, bad_chars):
    if sys.version_info > (3, 0):
        # For Python 3
        without_bad_chars = str.maketrans('', '', bad_chars)
        return s.translate(without_bad_chars)
    else:
        # For Python 2
        import string
        identity = string.maketrans('', '')
        return s.translate(identity, bad_chars)


def extract_data(html):
    """
    Extract the price history from the HTML.

    :param html: html having historical price data
    :return: end_date, start_date, headers(column name of data), rows(price data)
    """

    raw_data = pq(html)

    headers = [col.text_content().strip() for col in raw_data('tr')[0]]

    rows = []

    for _row in raw_data('tr')[1:]:
        row = [_native_type(_replace(col.text_content().strip(), ',-*?')) for col in _row.findall('td')]

        # change format of date ('Aug 24 2017' to '24-08-2017')
        row[0] = datetime.datetime.strptime(row[0], '%b %d %Y').strftime('%d-%m-%Y')

        rows.append(row)

    end_date, start_date = rows[0][0], rows[-1][0]

    return end_date, start_date, headers, rows


class InvalidParameters(ValueError):
    """Passed parameters are invalid."""


class InvalidCoinCode(NotImplementedError):
    """This coin code is unavailable on 'coinmarketcap.com'"""
