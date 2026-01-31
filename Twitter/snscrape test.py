import pprint
import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "Bitcoin"

for tweets in sntwitter.TwitterSearchScraper(query).get_items():
    pprint.pprint(tweets)
    break