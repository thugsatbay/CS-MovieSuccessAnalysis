import csv
import json
import requests
import time
from pathsANDkeys import PathsAndKeys as pak

init = pak()
google_path_folder = init.google
rotten_path_folder = init.rotten


def movie_db_individual_movie(movie_db_id):
    return "https://api.themoviedb.org/3/movie/" + str(movie_db_id) + "?api_key=0ffac534f18c20387c12c071460f72bd&language=en-US&append_to_response=external_ids"


years = init.years_list()


#Linked To IMDB
movie_db_time = 0
for each_year in years:
    print each_year
    with open(google_path_folder + "movie-" + str(each_year) + ".csv", "rb") as mv, open(google_path_folder + "movie-data-" + str(each_year) + ".csv", "wb") as md:
        reader = csv.reader(mv, delimiter = ',')
        writer = csv.writer(md)
        writer.writerow(['title_g','title','overview','production','release','revenue','budget','runtime','tagline','imdb','genres','poster'])
        row_index = 0
        for row in reader:
            row_index += 1
            database_table = []
            json_object = json.loads(row[2])["results"]
            json_movie_obj = json.loads(requests.get(movie_db_individual_movie(json_object[0]['id'])).content)
            #print row_index, json_movie_obj['title'].lower().replace(u"\xb7",".").replace(u"\xe9","e")
            database_table.extend((row[0],
            json_movie_obj['title'].lower().replace(u"\xb7",".").replace(u"\xe9","e"),
            json_movie_obj["overview"].encode("utf8"),
            json_movie_obj["production_companies"],
            json_movie_obj["release_date"],
            json_movie_obj["revenue"],
            json_movie_obj["budget"],
            json_movie_obj["runtime"],
            json_movie_obj["tagline"].encode("utf8"),
            json_movie_obj["imdb_id"],
            json_movie_obj["genres"],
            json_movie_obj["poster_path"]))
            writer.writerow(database_table)
            movie_db_time += 1
            if movie_db_time == 40:
                print "Application going into 10 seconds sleep for buffer time to moviedb ..."
                time.sleep(10)
                movie_db_time = 0
                print "Application awakened ..."


