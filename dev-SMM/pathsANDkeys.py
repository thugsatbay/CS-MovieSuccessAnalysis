class PathsAndKeys:
	
	def __init__(self):
		self.google = "./google-movies/"
		self.rotten = "./rotten-movies/"
		self.facebook = "./facebook-movies/"
		self.imdb = "./imdb-movies/"
		self.fb_app_id = 1365525390172605
		self.fb_app_secret = "ea1049f9dd56c57088a1cb410fd9878b" 
		self.start_year = 2008
		self.end_year = 2016


	def years_list(self):
		years = []
		for year in range(self.start_year, self.end_year + 1):
		    years.append(year)
		return years