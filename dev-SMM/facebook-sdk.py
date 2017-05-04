import facebook
from facepy import utils
from pathsANDkeys import PathsAndKeys as pak
import csv

init = pak()
google_path_folder = init.google
facebook_path_folder = init.facebook

fb_app_id = init.fb_app_id
fb_app_secret = init.fb_app_secret
oath_access_token = utils.get_application_access_token(fb_app_id, fb_app_secret)
years = init.years_list()


graph = facebook.GraphAPI(oath_access_token)
args = {'fields' : 'id, name, is_verified, fan_count, likes, engagement'}
movies_category = ['Movie', 'Fictional Character']
for each_year in years:
	print "\n",each_year,"\n"
	with open(google_path_folder + "movie-data-" + str(each_year) + ".csv", "rb") as mv, open(facebook_path_folder + "movie-data-" + str(each_year) + ".csv", "wb") as md:
		reader = csv.reader(mv, delimiter = ',')
		writer = csv.writer(md)
		writer.writerow(['title', 'title_f', 'likes', 'verified'])
		reader.next()
		for row in reader:
			all_pages = graph.request('/search?q=' + row[1].replace(" ","+") + '&type=page&fields=category&limit=50')['data']
			print row[1],", Fetching FB Likes ..."
			for page in all_pages:
				movie = graph.get_object(str(page['id']), **args)
				if page['category'] in movies_category and movie['is_verified']:
					#print all_pages,"\n"
					print [row[1], movie['name'].encode("utf8"), movie['engagement']['count'], movie['is_verified']]
					writer.writerow([row[1], movie['name'].encode("utf8"), movie['engagement']['count'], movie['is_verified']])
					#print all_pages
					#raw_input()#break
