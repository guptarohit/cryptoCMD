#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cryptocmd import CmcScraper

# Initialise scraper with 'coin code' of cryptocurrency
# If time interval is not passed all time data will be scrapped
scraper = CmcScraper("btc")

# You can pass name for the csv explicitly,
# Else it will be named in format {coin_code}_{start_date}_{end_date}.csv
scraper.export("csv", name="btc_all_time")
