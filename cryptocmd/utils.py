#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import datetime
from bs4 import BeautifulSoup
from requests import get


def get_url_data(url):
    """
    This method downloads the data of the webpage.
    :param url: 'url' of the webpage to download
    :return: response object of get request of the 'url'
    """

    try:
        response = get(url)
        return response
    except Exception as e:
        if hasattr(e, 'message'):
            print("Error message (get_url_data) :", e.message)
        else:
            print("Error message (get_url_data) :", e)


def get_coin_id(coin_code):
    """
    This method fetches the name(id) of currency from the given code
    :param coin_code: coin code of a cryptocurerncy e.g. btc
    :return: coin-id for the a cryptocurerncy on the coinmarketcap.com
    """

    try:
        url = 'https://api.coinmarketcap.com/v1/ticker/'

        json_resp = get_url_data(url).json()

        coin_code = coin_code.upper()

        for coin in json_resp:
            if coin['symbol'] == coin_code:
                return coin['id']
        raise InvalidCoinCode("This coin code is unavailable on 'coinmarketcap.com'")
    except Exception as e:
        raise e


def get_begin_latest_dates(coin_code):
    """
    Fetches the date (begin_date) since when the data is available on coinmarketcap.
    And date (latest_date) upto which data is available.
    :param coin_code: coin code of a cryptocurerncy e.g. btc
    :return: 'begin_date', 'latest_date' for given 'coin_code'
    """

    coin_code = coin_code.upper()

    coin_id = get_coin_id(coin_code)

    url = 'https://coinmarketcap.com/currencies/{0}/historical-data/'.format(coin_id)
    html = get_url_data(url).text

    begin_date = re.search("All Time': \[\"(.*)\"", html).group(1)
    begin_date = datetime.datetime.strptime(begin_date, '%m-%d-%Y')

    yesterday = datetime.date.today() - datetime.timedelta(1)
    latest_date = yesterday

    return begin_date.strftime('%d-%m-%Y'), latest_date.strftime('%d-%m-%Y')


def download_data(coin_code, start_date, end_date):
    """
    Download HTML price history for the specified cryptocurrency and time range from CoinMarketCap.

    :param coin_code: coin code of a cryptocurerncy e.g. btc
    :param start_date: date since when to scrape data (in the format of dd-mm-yyyy)
    :param end_date: date to which scrape the data (in the format of dd-mm-yyyy)
    :return: returns html of the webpage having historical data of cryptocurrency for certain duration
    """

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
            print("Error message: " + e.message)
        else:
            print('here', e)
            sys.exit(1)


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
        without_bad_chars = str.maketrans("", "", bad_chars)
        return s.translate(without_bad_chars)
    else:
        # For Python 2
        import string
        identity = string.maketrans("", "")
        return s.translate(identity, bad_chars)


def extract_data(html):
    """
    Extract the price history from the HTML.

    :param html: html having historical price data
    :return: headers(column name of data), rows (price data)
    """

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find("table", {"class": "table"})

    th_tags = table.find_all('th')
    headers = [th.get_text(strip=True) for th in th_tags]

    raw_rows = table.findAll('tr')

    rows = []
    for row in raw_rows:
        td_tags = row.find_all('td')
        if td_tags:
            rows.append([
                _native_type(_replace(td.get_text(strip=True), ',-*?')) for td in td_tags
            ])

    return headers, rows


class InvalidParameters(ValueError):
    """Passed parameters are invalid."""


class InvalidCoinCode(NotImplementedError):
    """This coin code is unavailable on 'coinmarketcap.com'"""
