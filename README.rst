.. -*-restructuredtext-*-

cryptoCMD: cryptoCurrency Market Data
======================================

.. image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
    :target: https://www.python.org/

.. image:: https://img.shields.io/pypi/v/cryptoCMD.svg
    :target: https://pypi.python.org/pypi/cryptoCMD

.. image:: https://travis-ci.org/guptarohit/cryptoCMD.svg?branch=master
    :target: https://travis-ci.org/guptarohit/cryptoCMD
    
.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fguptarohit%2FcryptoCMD.svg?type=shield
    :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fguptarohit%2FcryptoCMD?ref=badge_shield
    :alt: FOSSA Status

.. image:: https://img.shields.io/pypi/l/cryptoCMD.svg
    :target: https://github.com/guptarohit/cryptoCMD/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/pyversions/cryptoCMD.svg
    :target: https://pypi.python.org/pypi/cryptoCMD

.. image:: http://hits.dwyl.io/guptarohit/cryptoCMD.svg	
    :target: http://hits.dwyl.io/guptarohit/cryptoCMD
    :alt: HitCount

Cryptocurrency historical market price data scraper written in Python.


Installation
------------

::

    $ pip install cryptocmd

to install from the latest source use following command

::

    $ pip install git+git://github.com/guptarohit/cryptoCMD.git


Usage
------
=====================
CoinMarketCap Scraper
=====================

Following methods are available to get data in multiple formats from https://coinmarketcap.com

To get all time historical data of a cryptocurrency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from cryptocmd import CmcScraper

    # initialise scraper without passing time interval
    scraper = CmcScraper('XRP')

    # data as list of list in a variable
    headers, data = scraper.get_data()

    # export the data as csv file, you can also pass optional name parameter
    scraper.export_csv('xrp_all_time.csv')

    # Pandas dataFrame for the same data
    df = scraper.get_dataframe()

To get data of a cryptocurrency for some days
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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


Following are the columns of the data
"""""""""""""""""""""""""""""""""""""
``Date, Open, High, Low, Close, Volume, Market Cap``

Docker
------

To build the image, run 
``docker build -t crypto-cmd .```

Run like this
``docker run --rm -it crypto-cmd python samples/market-historical.py``

or also mount the current working directory to output the csv files into the current working directory
``docker run -v `pwd`:/usr/src --rm -it crypto-cmd python samples/market-historical.py``

Acknowledgements
----------------
The data is being scrapped from `coinmarketcap <https://coinmarketcap.com>`_ :v: and it's `free <https://coinmarketcap.com/faq/>`_ to use. :tada:

Contributing
------------

Feel free to make a pull request! :octocat:

License
-------

.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fguptarohit%2FcryptoCMD.svg?type=large
    :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fguptarohit%2FcryptoCMD?ref=badge_large
    :alt: FOSSA Status
