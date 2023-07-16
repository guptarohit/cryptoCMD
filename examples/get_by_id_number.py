#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cryptocmd import CmcScraper

# Initialise scraper with 'id_number' of cryptocurrency.
# 'id_number' is unique for each cryptocurrency, 
#   making it safer to retrieve data from tokens with duplicate names.
# 'id_number will override 'coin_code' and 'coin_name' when provided,
#   a WARNING will be printed if 'id_number' is provided 
#   and 'coin_code' or 'coin_name' provided are different from the coin returned.
# If time interval is not passed all time data will be scrapped
# 'id_number' can be retrieved from https://web-api.coinmarketcap.com/v1/cryptocurrency/map?symbol={SYMBOL}.
# following 'id_number' of sol coin retrieved from https://web-api.coinmarketcap.com/v1/cryptocurrency/map?symbol=sol

scraper = CmcScraper(id_number=5426)

# You can pass name for the csv explicitly,
# Else it will be named in format {coin_code}_{start_date}_{end_date}.csv
scraper.export("csv", name="sol_all_time")
