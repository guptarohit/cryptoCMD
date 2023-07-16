#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import datetime
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


def get_coin_id(coin_code, coin_name):
    """
    This method fetches the name(id) of currency from the given code
    :param coin_code: coin code of a cryptocurrency e.g. btc
    :param coin_name: coin name in case of many coins with same code e.g. sol -> solana, solcoin
    :return: coin-id for the a cryptocurrency on the coinmarketcap.com
    """

    api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/map?symbol={coin_code}".format(
        coin_code=coin_code
    )

    try:
        json_data = get_url_data(api_url).json()
        error_code = json_data["status"]["error_code"]
        if error_code == 0:
            if coin_name is None:
                return json_data["data"][0]["slug"]

            return [data["slug"] for data in json_data["data"] if data["name"].lower() == coin_name.lower()][0]
        if error_code == 400:
            raise InvalidCoinCode(
                "'{}' coin code is unavailable on coinmarketcap.com".format(coin_code)
            )
        else:
            raise Exception(json_data["status"]["error_message"])
    except Exception as e:
        print("Error fetching coin id data for coin code {}".format(coin_code))

        if hasattr(e, "message"):
            print("Error message:", e.message)
        else:
            print("Error message:", e)


def download_coin_data(coin_code, start_date, end_date, fiat, coin_name, id_number=None):
    """
    Download HTML price history for the specified cryptocurrency and time range from CoinMarketCap.

    :param coin_code: coin code of a cryptocurrency e.g. btc
    :param start_date: date since when to scrape data (in the format of dd-mm-yyyy)
    :param end_date: date to which scrape the data (in the format of dd-mm-yyyy)
    :param fiat: fiat code eg. USD, EUR
    :param coin_name: coin name in case of many coins with same code e.g. sol -> solana, solcoin
    :param id_number: id number for the token on coinmarketcap. Will override coin_code and coin_name when provided.

    :return: returns html of the webpage having historical data of cryptocurrency for certain duration
    """

    if start_date is None:
        # default start date on coinmarketcap.com
        start_date = "28-4-2013"

    if end_date is None:
        yesterday = datetime.date.today() - datetime.timedelta(1)
        end_date = yesterday.strftime("%d-%m-%Y")

    if not id_number:
        coin_id = get_coin_id(coin_code, coin_name)

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

    if id_number:
        api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert={}&id={}&time_end={}&time_start={}".format(
            fiat, id_number, end_date_timestamp, start_date_timestamp
        )
    else:
        api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert={}&slug={}&time_end={}&time_start={}".format(
            fiat, coin_id, end_date_timestamp, start_date_timestamp
        )

    try:
        json_data = get_url_data(api_url).json()
        if json_data["status"]["error_code"] != 0:
            raise Exception(json_data["status"]["error_message"])
        if id_number:
            show_coin_info = False
            if coin_code and coin_code != json_data['data']['symbol']:
                print(f"INFO: Using 'id_number'! The 'coin_code' ({coin_code}) provided " + \
                      "is different from the symbol returned.")
                show_coin_info = True
            if coin_name and coin_name != json_data['data']['name']:
                print(f"INFO: Using 'id_number'! The 'coin_name' ({coin_name}) provided " + \
                      "is different from the symbol returned.")
                show_coin_info = True
            if show_coin_info:
                print(f"""The returned data belongs to coin "{json_data['data']['name']}", """ + \
                        f"""with symbol "{json_data['data']['symbol']}" """)
        return json_data
    except Exception as e:
        print(
            "Error fetching price data for {} for interval '{}' and '{}'".format(
            f"(id {id_number})" if id_number else coin_code,
            start_date,
            end_date,
        ))

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
