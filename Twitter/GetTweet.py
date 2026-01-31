import pprint

import requests
from requests_oauthlib import OAuth1


auth1 = OAuth1("7IyXPfj0alamtHKd3He8zjOGx", "eBKwW18KwcETol2VPzK4McATLMRYJJPTc0BsyKbjWFniKIFWZD",  "1771177480059240448-ERN4cRp1e3y2tgHZwkxn6eusgeu5RM", "vC5SlJHC4K6mPIWK6nPJg88q5tJLym3SDhtVcAZYN4V6n")
try:

    tweet_data = {
        'query': "bitcoin ethereum memecoin slerf grok crypto bullrun meme dog",
    }
    response = requests.get('https://api.twitter.com/2/users/by/username/saintquinok', auth=auth1, json=tweet_data)
    if response.status_code == 403:
        print(response.text)
    else:
        pprint.pprint(response)



except requests.exceptions.RequestException as e:
    print(e, "a")
