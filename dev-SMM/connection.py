import tweepy
'''
Authorization Code
'''
class twitter:

	def __init__(self):
		self.twitter_consumer_key="7jOddgbMJHee54UU0DhzCcaeD"
		self.twitter_consumer_secret="OAUcR5McjDZ7vlIHtIJaPRkaepBp1Ad6ATReG4i8EnCiCrwmYf"
		self.twitter_access_token="2217656720-0u9ZLcqYf7pRIm6IFhWU93NxvSusK3P67w9n1tz"
		self.twitter_access_token_secret="kgw5GQUcMgM92HPfroVYgFZPYkMm5GjfHfIVZyxRcP37w"
		print "Initializing twitter ..."
		print "Initializing done"

	def connect(self):
		auth = tweepy.OAuthHandler(self.twitter_consumer_key, self.twitter_consumer_secret)
		auth.set_access_token(self.twitter_access_token, self.twitter_access_token_secret)
		api = tweepy.API(auth)
		print api.me().name
		print "Authentication was successful!"