cryptoCMD: cryptoCurrency Market Data
======================================

.. image:: https://img.shields.io/pypi/v/cryptoCMD.svg
    :target: https://pypi.python.org/pypi/cryptoCMD

.. image:: https://img.shields.io/pypi/l/cryptoCMD.svg
    :target: https://pypi.python.org/pypi/cryptoCMD

.. image:: https://img.shields.io/pypi/wheel/cryptoCMD.svg
    :target: https://pypi.python.org/pypi/cryptoCMD

.. image:: https://img.shields.io/pypi/pyversions/cryptoCMD.svg
    :target: https://pypi.python.org/pypi/cryptoCMD

.. image:: http://hits.dwyl.io/guptarohit/cryptoCMD.svg
    :target: http://hits.dwyl.io/guptarohit/cryptoCMD


Cryptocurrency historical market price data scrapper written in Python 3.

Usage
------
=====================
CoinMarketCap Scraper
=====================

Following methods available to get data in multiple formats from https://coinmarketcap.com

.. code:: python

    from cryptocmd import CmcScraper

    # initialise scraper
    scraper = CmcScraper('XRP', '15-10-2017', '25-10-2017')

    # get data as list of list
    headers, data = scraper.get_data()

    # export the data to csv
    scraper.export_csv()

    # get dataframe for the data
    df = scraper.get_dataframe()


Installation
------------

::

    $ pip install cryptocmd


Contributing
------------

Feel free to make a pull request!
