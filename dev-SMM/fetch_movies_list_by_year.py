from bs4 import BeautifulSoup
from pathsANDkeys import PathsAndKeys as pak
import csv
import requests
import urllib2
import re
import time

google_movies_folder_path = "./google-movies-files/"
init = pak()
rotten_tomatoes_output_folder_path = init.rotten
google_movies_output_folder_path = init.google
years = init.years_list()

def wikipedia_connection_string():
    return "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"

def movie_db_connection_string(movie_db_query ,movie_db_year):
    return "https://api.themoviedb.org/3/search/movie?api_key=0ffac534f18c20387c12c071460f72bd&language=en-US&query=" + movie_db_query + "&page=1&include_adult=true&region=US&year=" + movie_db_year + "&primary_release_year=" + movie_db_year

def movies_html(query):
    return BeautifulSoup((requests.get(query)).content, 'lxml')

def rotten_tomatoes_movies():
    print "Fetch Rotten Tomatoes Top 100 Movie List"
    for each_year in years:
        database_year = []
        rotten_movie_query = "https://www.rottentomatoes.com/top/bestofrt/?year=" + str(each_year)
        soup = movies_html(rotten_movie_query).find_all("table",{"class":"table"})
        soup = BeautifulSoup(str(soup), "html.parser").find_all("tr")
        for each_row in soup:
            row = BeautifulSoup(str(each_row), "html.parser")
            if row.td != None:
                database_year.append([row.find("td", {"class":"right hidden-xs"}).string,
                row.find("a", {"class":"unstyled articleLink"}).string.strip()
                .replace("\\n","").replace("(" + str(each_year) + ")","").strip().lower(),
                row.find("span",{"class":"tMeterScore"}).string[-3:-1],
                str(row.find("a", {"class":"unstyled articleLink"})["href"])])
        with open(rotten_tomatoes_output_folder_path + "movie-" + str(each_year) + ".csv", "wb") as mv:
            writer = csv.writer(mv)
            for entry in database_year:
                writer.writerow(entry)
        print str(each_year), "File Completed"


def google_movies():
    print "Fetch Google Top 51 movies List with moviedb Info"
    movie_db_time = 0
    for each_year in years:
        with open(google_movies_folder_path + str(each_year) + ".html", "rb") as html_file:
            database_year = []
            soup = BeautifulSoup(html_file, "lxml")
            soup = soup.find_all(attrs={'class': re.compile(r"^_GCg")})
            image_link, movie_name, movie_info = "", "", ""
            for entry in soup:
                if entry.img.has_attr('data-key'):
                    image_link = entry.img['data-key']
                elif entry.img.has_attr('data-src'):
                    image_link = entry.img['data-src']
                movie_name = (" ".join([title.string.strip().replace(u"\u2019", "'").replace(u"\u2013", "").replace(u"\xe9", "e") 
                    for title in (BeautifulSoup(str(entry), "lxml").find_all("span"))])).lower()
                movie_info = str(requests.get(movie_db_connection_string(str(movie_name.replace(" ","%20")),str(each_year))).content)
                database_year.append([movie_name, image_link, movie_info])
                movie_db_time += 1
                if movie_db_time == 40:
                    print "Sleeping for 10 seconds to refresh MovieDB buffer ..."
                    time.sleep(10)
                    print "Process Awakened ..."
                    movie_db_time = 0
            with open(google_movies_output_folder_path + "movie-" + str(each_year) + ".csv", "wb") as mv:
                writer = csv.writer(mv)
                for line in database_year:
                   #print line[0].replace('\\u',"'")
                   writer.writerow(line)
            print str(each_year),"File Completed"


google_movies()
rotten_tomatoes_movies()