from imdb import IMDb
from pathsANDkeys import PathsAndKeys as pak
from bs4 import BeautifulSoup
import requests
import csv

google_folder_path = init.google
imdb_output_folder_path = init.imdb
years = init.years_list()

def imdb_review_query(imdb_movie_id):
	return "http://www.imdb.com/title/" + imdb_movie_id + "/reviews?ref_=tt_urv"

'''
def collect_imdb_review(imdb_movie_id):
	soup = BeautifulSoup(requests.get(imdb_review_query(imdb_movie_id)).content, "lxml").find("div",{"id":"tn15content"})
	all_info = soup.find_all("small")
	all_reviews = soup.find_all("p")
	temp = []
	for p in all_reviews:
		if len(str(p)) > imdb_good_review_length:
			temp.append(p)
	all_reviews = temp
	imp = 0
	temp = []
	for div in all_info:
		if imp % 3 == 0:
			temp.append(div)
		imp += 1
	all_info = temp
	print len(all_reviews), len(all_info)

	#print len(all_p)
	#for p in all_p:
	#	print p
	#	print ""

collect_imdb_review('tt0468569')
'''

ia = IMDb()
for each_year in years:
	print each_year
	with open(google_path_folder + "movie-data-" + str(each_year) + ".csv", "rb") as mv:
		reader = csv.reader(mv, delimiter = ',')
		reader.next()
		for row in reader:
			movie = ia.get_movie(int(row[9].replace("tt","")))
			movie['title']
			movie['year']
			movie['director']
			movie['cast']
			movie['plot']
			movie['rating']
			movie['votes']
			movie['genres']
			movie['mpaa']
			print row[0]
			raw_input()