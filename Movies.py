import csv
import requests
import re
import pickle

DATAPATH = 'ml-latest-small/movies.csv'
FILEPATH = 'movies.txt'
APIKEY = 'aa03d634'


class Movie:
    def __init__(self, title, people):
        self.title = title
        self.people = people


def read_movies():
    with open(DATAPATH, 'r') as fr, open(FILEPATH, 'w') as fw:
        data = csv.reader(fr)
        for row in data:
            movie = row[1].rsplit(' ', 1)[0].strip()
            the_regex = re.compile(r'(.*?), The')
            try:
                movie_new = the_regex.search(movie).group(1)
                movie = "The " + movie_new
            except AttributeError:
                pass
            bracket_regex = re.compile(r'(.*)\(.*?\)')
            try:
                movie_new = bracket_regex.search(movie).group(1)
                movie = movie_new
            except AttributeError:
                pass
            # try:
            #     movie_new = regex.search(movie)
            # fw.write(row[1].rsplit(' ', 1)[0])
            fw.write(movie)
            fw.write('\n')


def get_movies_data():
    with open(FILEPATH, 'r') as f:
        data = f.read()
    movies = data.split('\n')
    regex = re.compile(r'(.*)?\(.*?\)')
    movies_obj = load_movies_data()
    movie_titles = [movie.title for movie in movies_obj]
    for movie in movies:
        response = requests.get('http://www.omdbapi.com',
                                params={'apikey': APIKEY, 't': movie})
        response.raise_for_status()
        print(movie)
        # print(response.content)
        json_response = response.json()
        print("Title: ")
        try:
            print(json_response["Title"])
        except KeyError:
            print("Move not found")
            continue
        if movie in movie_titles:
            continue
        directors = json_response["Director"].split(', ')
        # for director in directors:
        for i in range(len(directors)):
            try:
                directors[i] = regex.search(directors[i]).group(1)
            except AttributeError:
                pass
            directors[i] = directors[i].strip()
        writers = json_response["Writer"].split(', ')
        for i in range(len(writers)):
            try:
                writers[i] = regex.search(writers[i]).group(1)
            except AttributeError:
                pass
            writers[i] = writers[i].strip()
        actors = json_response["Actors"].split(', ')
        for i in range(len(actors)):
            try:
                actors[i] = regex.search(actors[i]).group(1)
            except AttributeError:
                pass
            actors[i] = actors[i].strip()
        # Deduplication of all the lists and merging them to a single list of people
        people = []
        for director in directors:
            if director not in people:
                people.append(director)
        for writer in writers:
            if writer not in people:
                people.append(writer)
        for actor in actors:
            if actor not in people:
                people.append(actor)
        print(people)
        movie_obj = Movie(movie, people)
        with open("movies.pickle", "ab") as f:
            pickle.dump(movie_obj, f)


def load_movies_data():
    movies = []
    with open("movies.pickle", "rb") as f:
        while True:
            try:
                movie = pickle.load(f)
                movies.append(movie)
                # print(movie.title)
                # print(movie.people)
            except EOFError:
                break
    return movies


if __name__ == "__main__":
    # read_movies()
    get_movies_data()
    # load_movies_data()
