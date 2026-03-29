#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import datetime
from requests import get


# CoinMarketCap internal data API base URL (replaces the defunct web-api.coinmarketcap.com).
_CMC_DATA_API = "https://api.coinmarketcap.com/data-api/v3"

# CMC fiat currency IDs used in convertId parameter.
_FIAT_IDS = {
    "USD": 2781,
    "EUR": 2790,
    "GBP": 2791,
    "JPY": 2797,
    "AUD": 2782,
    "CAD": 2784,
    "CHF": 2785,
    "CNY": 2787,
}

_HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_url_data(url):
    """
    This method downloads the data of the web page.
    :param url: 'url' of the web page to download
    :return: response object of get request of the 'url'
    """

    try:
        response = get(url, headers=_HEADERS)
        return response
    except Exception as e:
        if hasattr(e, "message"):
            print("Error message (get_url_data) :", e.message)
        else:
            print("Error message (get_url_data) :", e)
        raise e


def get_coin_id(coin_code, coin_name):
    """
    This method fetches the numeric CMC ID for a given coin symbol.
    :param coin_code: coin code of a cryptocurrency e.g. BTC
    :param coin_name: coin name to disambiguate when multiple coins share a symbol
    :return: numeric CMC coin ID (int) for the cryptocurrency
    """

    api_url = "{}/cryptocurrency/listing?start=1&limit=5000&sortBy=market_cap&sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false".format(
        _CMC_DATA_API
    )

    try:
        json_data = get_url_data(api_url).json()
        coins = json_data["data"]["cryptoCurrencyList"]

        symbol_upper = coin_code.upper()
        matches = [c for c in coins if c["symbol"].upper() == symbol_upper]

        if not matches:
            raise InvalidCoinCode(
                "'{}' coin code is unavailable on coinmarketcap.com".format(coin_code)
            )

        if coin_name is not None:
            named = [c for c in matches if c["name"].lower() == coin_name.lower()]
            if named:
                return named[0]["id"]

        # Return the highest-ranked (by market cap) match.
        return matches[0]["id"]

    except InvalidCoinCode:
        raise
    except Exception as e:
        print("Error fetching coin id data for coin code {}".format(coin_code))

        if hasattr(e, "message"):
            print("Error message:", e.message)
        else:
            print("Error message:", e)


def download_coin_data(
    coin_code, start_date, end_date, fiat, coin_name, id_number=None
):
    """
    Download historical OHLCV + market cap data for the specified cryptocurrency from CoinMarketCap.

    :param coin_code: coin code of a cryptocurrency e.g. btc
    :param start_date: date since when to scrape data (in the format of dd-mm-yyyy)
    :param end_date: date to which scrape the data (in the format of dd-mm-yyyy)
    :param fiat: fiat code eg. USD, EUR
    :param coin_name: coin name in case of many coins with same code e.g. sol -> solana, solcoin
    :param id_number: numeric CMC ID for the token; overrides coin_code/coin_name lookup when provided.

    :return: parsed JSON response from CMC data API
    """

    if start_date is None:
        # default start date on coinmarketcap.com
        start_date = "28-4-2013"

    if end_date is None:
        yesterday = datetime.date.today() - datetime.timedelta(1)
        end_date = yesterday.strftime("%d-%m-%Y")

    coin_id = id_number if id_number else get_coin_id(coin_code, coin_name)

    convert_id = _FIAT_IDS.get(fiat.upper(), _FIAT_IDS["USD"])

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

    api_url = "{}/cryptocurrency/historical?id={}&convertId={}&timeStart={}&timeEnd={}".format(
        _CMC_DATA_API, coin_id, convert_id, start_date_timestamp, end_date_timestamp
    )

    try:
        json_data = get_url_data(api_url).json()
        status = json_data.get("status", {})
        error_code = status.get("error_code")
        if error_code and str(error_code) != "0":
            raise Exception(status.get("error_message", "Unknown error"))

        if id_number:
            show_coin_info = False
            returned_symbol = json_data["data"].get("symbol", "")
            returned_name = json_data["data"].get("name", "")
            if coin_code and coin_code.upper() != returned_symbol.upper():
                print(
                    "INFO: Using 'id_number'! The 'coin_code' ({}) provided ".format(coin_code)
                    + "is different from the symbol returned."
                )
                show_coin_info = True
            if coin_name and coin_name.lower() != returned_name.lower():
                print(
                    "INFO: Using 'id_number'! The 'coin_name' ({}) provided ".format(coin_name)
                    + "is different from the name returned."
                )
                show_coin_info = True
            if show_coin_info:
                print(
                    'The returned data belongs to coin "{}", '.format(returned_name)
                    + 'with symbol "{}"'.format(returned_symbol)
                )

        return json_data
    except Exception as e:
        print(
            "Error fetching price data for {} for interval '{}' and '{}'".format(
                "(id {})".format(id_number) if id_number else coin_code,
                start_date,
                end_date,
            )
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
