from django.db import models


# Create your models here.
class Node(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserInput(models.Model):
    nodes = models.ManyToManyField(Node)

# class Person(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


# class Genre(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


# class Movie(models.Model):
#     title = models.CharField(max_length=100)
#     people = models.ManyToManyField(Person)
#     genres = models.ManyToManyField(Genre)
#
#     def __str__(self):
#         return self.title
