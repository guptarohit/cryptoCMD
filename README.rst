cryptoCMD: cryptoCurrency Market Data
======================================

Cryptocurrency historical market price data scrapper written in Python 3.

Installation
------------

::

    $ pip install cryptocmd

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

Contributing
------------

Feel free to make a pull request!
