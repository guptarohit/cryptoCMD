from cryptocmd import CmcScraper

# initialise scraper without passing time interval
scraper = CmcScraper('XRP')

# data as list of list in a variable
headers, data = scraper.get_data()

# export the data as csv file, you can also pass optional name parameter
scraper.export_csv('xrp_all_time.csv')

# Pandas dataFrame for the same data
df = scraper.get_dataframe()
print(df)
