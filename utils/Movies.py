import csv
import requests
import re
import pickle
from bs4 import BeautifulSoup
from decouple import config

DATAPATH = 'ml-latest-small/movies.csv'
FILEPATH = 'movies.txt'
APIKEY = config('APIKEY')


class Movie:
    def __init__(self, title, people, genres):
        self.title = title
        self.people = people
        self.genres = genres


def read_movies_dataset():
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
    try:
        movies_obj = load_movies_data()
    except FileNotFoundError:
        movies_obj = []
    movie_titles = [movie.title for movie in movies_obj]
    exit = False
    left_movies = []
    for movie in movies:
        if exit:
            left_movies.append(movie)
            continue
        response = requests.get('http://www.omdbapi.com',
                                params={'apikey': APIKEY, 't': movie})
        try:
            response.raise_for_status()
        except Exception:
            exit = True
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
        genres = json_response['Genre']
        genres = genres.split(',')
        for i in range(len(genres)):
            genres[i] = genres[i].strip()
        print(genres)
        movie_obj = Movie(movie, people, genres)
        with open("movies.pickle", "ab") as f:
            pickle.dump(movie_obj, f)
    if exit:
        with open(FILEPATH, 'w') as f:
            for movie in left_movies:
                f.write(movie)
                f.write('\n')


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


def movies_to_nodes():
    movies = load_movies_data()
    nodes = []
    for movie in movies:
        # print(movies[0])
        nodes.append(movie.title)
        for person in movie.people:
            if person not in nodes:
                nodes.append(person)
        for genre in movie.genres:
            if genre not in nodes:
                nodes.append(genre)
    with open("nodes.pickle", "wb") as f:
        pickle.dump(nodes, f)
    return nodes


def load_nodes():
    with open("nodes.pickle", "rb") as f:
        nodes = pickle.load(f)
    return nodes


def load_movie_titles():
    with open("imdb_movies.txt", "r") as f:
        movies = f.read().split("\n")
    for i in range(len(movies)):
        movies[i] = movies[i].strip()
    return movies
    # titles = []
    # with open("movies.pickle", "rb") as f:
    #     while True:
    #         try:
    #             movie = pickle.load(f)
    #             titles.append(movie.title)
    #         except EOFError:
    #             break
    # return titles


def get_movies_imdb():
    imdb_url = 'https://www.imdb.com/list/ls063540474/?sort=list_order,asc&st_dt=&mode=detail'
    pages = 2
    movies = []
    for i in range(1, pages + 1):
        res = requests.get(imdb_url, params={'page': i})
        res.raise_for_status()
        res = res.text
        soup = BeautifulSoup(res, 'lxml')
        img_html_list = soup.select('img[class="loadlate"]')
        for img_html in img_html_list:
            movie = img_html.get('alt')
            movies.append(movie)
    with open(FILEPATH, 'w') as f:
        for movie in movies:
            print(movie)
            f.write(movie)
            f.write('\n')


def get_movies_tmdb():
    tmdb_url = 'https://www.themoviedb.org/movie'
    pages = 500
    movies = []
    for i in range(1, pages + 1):
        res = requests.get(tmdb_url, params={'page': i})
        res.raise_for_status()
        res = res.text
        soup = BeautifulSoup(res, 'lxml')
        a_html_list = soup.select('a[class="result"]')
        for a_html in a_html_list:
            movie = a_html.get('alt')
            movies.append(movie)
    with open(FILEPATH, 'w') as f:
        for movie in movies:
            print(movie)
            f.write(movie)
            f.write('\n')


def get_movies_cinestaan():
    pages = 2
    movies = []
    for i in range(1, pages + 1):
        url = 'https://www.cinestaan.com/movies/hindi/released/latest/{}/10000'.format(
            i)
        res = requests.get(url)
        print(url)
        res.raise_for_status()
        res = res.text
        soup = BeautifulSoup(res, 'lxml')
        a_html_list = soup.select('a[property="name"]')
        for a_html in a_html_list:
            movie = a_html.text
            movie = movie.split('\n')[0]
            movie = movie.rsplit(' ', 1)[0].strip()
            movies.append(movie)
    with open(FILEPATH, 'w') as f:
        for movie in movies:
            print(movie)
            f.write(movie)
            f.write('\n')


if __name__ == "__main__":
    pass
    # read_movies_dataset()
    # pass
    # movies_to_nodes()
    # read_movies()
    # get_movies_data()
    # get_movies_imdb()
    # get_movies_tmdb()
    # get_movies_cinestaan()
    # movies = load_movies_data()
    # for movie in movies:
    #     print(movie.title)
    #     print(movie.genres)
    #     print(movie.people)
    #     print(type(movie))
