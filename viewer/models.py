import string
from xmlrpc.client import DateTime

from django.db import models
from django.db.models import Model, CharField, DateField

# Create your models here.

""" MODELS

Genre
- name: string

Country
- name: string
- code: string

Creator
- name: string
- surname: string
- date_of_birth: Date
- date_of_death: Date
- country_of_birth: Country
- country_of_death: Country
- biography: string

Movie
- title_orig: string
- title_cz: string
- genres: List[Genre]
- countries: List[Country]
- actors: List[Creator]
- directors: List[Creator]
# TODO: Music, Script, ...
- length: int(min)
- released: int(year)
- description: string
- rating: float (výpočet z review)
- created: DateTime
- updated: DateTime

Review
- UserProfile: Profile
- movie: Movie
- review: string
- rating: int(0-100)

"""


class Genre(Model):
    name = CharField(max_length=20)


    def __repr__(self):
        return f"Genre(name={self.name})"


    def __str__(self):
        return f"{self.name}"


class Country(Model):
    name = CharField(max_length=32)
    code = CharField(max_length=3)


class Creator(Model):
    name = CharField(max_length=32)
    surname = CharField(max_length=32)
    date_of_birth = DateField()
    date_of_death = DateField()
    country_of_birth: Country
    country_of_death: Country
    biography = CharField(max_length=255)


class Movie(Model):
    title_orig = CharField(max_length=150)
    title_cz = CharField(max_length=128)
    genres: [Genre]
    countries: [Country]
    actors: [Creator]
    directors: [Creator]
    length: int
    released: int
    description: CharField(max_length=255)
    rating: float
    created_record: DateTime
    updated_record: DateTime
