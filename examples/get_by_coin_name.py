#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cryptocmd import CmcScraper

# Initialise scraper with 'coin code' and 'coin name' of cryptocurrency
# Need to pass both in case other coin(s) have same code
# If time interval is not passed all time data will be scrapped
scraper = CmcScraper(coin_code="sol", coin_name="solana")

# You can pass name for the csv explicitly,
# Else it will be named in format {coin_code}_{start_date}_{end_date}.csv
scraper.export("csv", name="solana_all_time")
