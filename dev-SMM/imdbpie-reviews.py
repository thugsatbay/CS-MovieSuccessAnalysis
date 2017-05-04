from imdbpie import Imdb as im
from imdb import IMDb
from pathsANDkeys import PathsAndKeys as pak
import csv

init = pak()
imdb = im()

google_folder_path = init.google
imdb_output_folder_path = init.imdb
NO_OF_REVIEWS = 25
years = init.years_list()

def fetch_imdb_reviews():
	for each_year in years:
		print each_year
		with open(google_folder_path + "movie-data-" + str(each_year) + ".csv", "rb") as rf, open(imdb_output_folder_path + "movie-data-" + str(each_year) + ".csv", "wb") as wf:
			reader = csv.reader(rf, delimiter = ',')
			writer = csv.writer(wf)
			reader.next()
			for row in reader:
				output_row = []
				output_row.append([])
				title_id = str(row[9])
				print title_id
				if imdb.title_exists(title_id):
					title = imdb.get_title_by_id(title_id)
					name = title.title
					rating = title.rating
					cert = title.certification
					if cert == "" or cert == None:
						cert = ""
					reviews = imdb.get_title_reviews(title_id, max_results = NO_OF_REVIEWS)
					review_file_path = imdb_output_folder_path + "/reviews/movie-" + title_id
					if reviews != None:
						if len(reviews) >= 1:
							with open(review_file_path, "w") as review_write:
								review_write.write("### Seperation : (text, date, rating, summary, status, user_score, user_score_count) $$$ End of review \n")
								for each_review in reviews:
									review_write.write(each_review.text.encode("utf8"))
									review_write.write("\n###\n")
									review_write.write(str(each_review.date))
									review_write.write("\n###\n")
									review_write.write(str(each_review.rating))
									review_write.write("\n###\n")
									review_write.write(each_review.summary.encode("utf8"))
									review_write.write("\n###\n")
									review_write.write(str(each_review.status))
									review_write.write("\n###\n")
									review_write.write(str(each_review.user_score))
									review_write.write("\n###\n")
									review_write.write(str(each_review.user_score_count))
									review_write.write("\n$$$\n")
						else:
							review_file_path = ""
					else:
						review_file_path = ""
					writer.writerow([title_id, name.encode("utf8"), rating, cert.encode("utf8"), review_file_path.encode("utf8")])
					print name, "movie processed ..."



def imdb_details():
	ia = IMDb()
	for each_year in years:
		print each_year
		with open(google_folder_path + "movie-data-" + str(each_year) + ".csv", "rb") as rf, open(imdb_output_folder_path + "movie-info-" + str(each_year) + ".csv", "wb") as wf:
			reader = csv.reader(rf, delimiter = ',')
			writer = csv.writer(wf)
			reader.next()
			writer.writerow(['imdb_id', 'title', 'year', 'plot', 'rating', 'votes', 'genres', 'people', 'mpaa'])
			for row in reader:
				cast_movie = imdb.get_title_by_id(row[9])
				movie = ia.get_movie(int(row[9].replace("tt","")))
				print cast_movie.title, "Processing ..."
				output = []
				people = {}
				for person in cast_movie.credits:
					if person.token in people:
						people[person.token].append([person.name,person.imdb_id])
					else:
						people[person.token] = [[person.name,person.imdb_id]]
				output.append(row[9].encode("utf8"))
				output.append(movie['title'].encode("utf8"))
				output.append(movie['year'])
				if 'plot' in movie:
					output.append(movie['plot'])
				else:
					output.append("")
				output.append(movie['rating'])
				if 'votes' in movie:
					output.append(movie['votes'])
				else:
					output.append("")
				output.append(movie['genres'])
				output.append(people)
				if 'mpaa' in movie:
					output.append(movie['mpaa'])
				else:
					output.append("")
				writer.writerow(output)
				#raw_input()


#fetch_imdb_reviews()
imdb_details()

