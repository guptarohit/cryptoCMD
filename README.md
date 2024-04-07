# cryptoCMD: cryptoCurrency Market Data

[![PyPI Version][]][1] [![CI Status][]][2] [![License][]][3] [![Downloads][]][4] [![Ruff][]][5] [![GitHub Sponsors][]][6]


Cryptocurrency historical market price data scraper written in Python.

## Installation

```sh
pip install cryptocmd
```

to install from the latest source use following command

```sh
pip install git+git://github.com/guptarohit/cryptoCMD.git
```

## Usage

### CoinMarketCap Scraper

Following methods are available to get data in multiple formats from
<https://coinmarketcap.com>

#### To get all time historical data of a cryptocurrency

```python
from cryptocmd import CmcScraper

# initialise scraper without time interval
scraper = CmcScraper("XRP")

# get raw data as list of list
headers, data = scraper.get_data()

# get data in a json format
xrp_json_data = scraper.get_data("json")

# export the data as csv file, you can also pass optional `name` parameter
scraper.export("csv", name="xrp_all_time")

# Pandas dataFrame for the same data
df = scraper.get_dataframe()
```

#### To get data of a cryptocurrency which have same coin code as others

```python
from cryptocmd import CmcScraper

# initialise scraper with coin name as well
scraper = CmcScraper(coin_code="sol", coin_name="solana")

# get raw data as list of list
headers, data = scraper.get_data()

# get data in a json format
solana_json_data = scraper.get_data("json")

# export the data as csv file, you can also pass optional `name` parameter
scraper.export("csv", name="solana_all_time")

# Pandas dataFrame for the same data
df = scraper.get_dataframe()
```

#### To get data of a cryptocurrency for some days

```python
from cryptocmd import CmcScraper

# initialise scraper with time interval
scraper = CmcScraper("XRP", "15-10-2017", "25-10-2017")

# get raw data as list of list
headers, data = scraper.get_data()

# get data in a json format
json_data = scraper.get_data("json")

# export the data to csv
scraper.export("csv")

# get dataframe for the data
df = scraper.get_dataframe()
```

##### Following are the columns of the data

`Date, Open, High, Low, Close, Volume, Market Cap, Time Open, Time High, Time Low, Time Close`

## Acknowledgements

The data is being scrapped from
[coinmarketcap](https://coinmarketcap.com) :v: and it\'s
[free](https://coinmarketcap.com/faq/) to use. :tada:

## Contributing

Feel free to make a pull request! :octocat:

If you found this useful, I\'d appreciate your consideration in the
below. ✨☕


[PyPI Version]: https://img.shields.io/pypi/v/cryptoCMD.svg
[1]: https://pypi.python.org/pypi/cryptoCMD
[CI Status]: https://github.com/guptarohit/cryptoCMD/actions/workflows/ci.yml/badge.svg
[2]: https://github.com/guptarohit/cryptoCMD/actions/workflows/ci.yml
[License]: https://img.shields.io/pypi/l/cryptoCMD.svg
[3]: https://github.com/guptarohit/cryptoCMD/blob/master/LICENSE
[Downloads]: https://pepy.tech/badge/cryptoCMD
[4]: https://pepy.tech/project/cryptoCMD
[Ruff]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[5]: https://github.com/astral-sh/ruff
[GitHub Sponsors]: https://img.shields.io/github/sponsors/guptarohit?color=%23FF5733
[6]: https://github.com/sponsors/guptarohit
[![Buy Me A Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=rohitgupta&button_colour=5F7FFF&font_colour=ffffff&font_family=Lato&outline_colour=000000&coffee_colour=FFDD00)](https://www.buymeacoffee.com/rohitgupta)
