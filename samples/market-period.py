from cryptocmd import CmcScraper

# initialise scraper
scraper = CmcScraper('XRP', '15-10-2017', '25-10-2017')

# get data as list of list
headers, data = scraper.get_data()

# export the data to csv
scraper.export_csv('market-period.csv')

# get dataframe for the data
df = scraper.get_dataframe()
print(df)
