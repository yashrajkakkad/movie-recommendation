from django.shortcuts import render, HttpResponse
from dal import autocomplete
from .models import Movie, Person, Genre
from itertools import chain


# Create your views here.
def home(request):
    return HttpResponse("Home page comes here!")


class MovieAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Movie.objects.none()
        movie_qs = Movie.objects.all()
        person_qs = Person.objects.all()
        genre_qs = Genre.objects.all()
        qs = None
        if self.q:
            movie_qs = movie_qs.filter(title__startswith=self.q)
            person_qs = person_qs.filter(name__startswith=self.q)
            genre_qs = genre_qs.filter(name__startswith=self.q)
            qs = list(chain(movie_qs, person_qs, genre_qs))
        return qs