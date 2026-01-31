import twint


t = twint.Config()
t.Search = "Bitcoin"
t.Limit = 1000
t.Min_likes = 2000
t.Min_retweets = 100

twint.run.Search(t)
