from django.contrib import admin
from .models import Movie, Person, Genre

# Register your models here.
admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Genre)
