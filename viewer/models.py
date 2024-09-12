from datetime import date
from platform import release
from xmlrpc.client import DateTime

from django.db import models
from django.db.models import Model, CharField, DateField, ForeignKey, SET_NULL, TextField, ManyToManyField, \
    IntegerField, FloatField, DateTimeField

# Create your models here.
class Genre(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)


    class Meta:
        ordering = ['name']


    def __repr__(self):
        return f"Genre(name={self.name})"


    def __str__(self):
        return f"{self.name}"


class Country(Model):
    name = CharField(max_length=64, null=False, blank=False, unique=True)
    code = CharField(max_length=3, null=False, blank=False, unique=True)


    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']


    def __repr__(self):
        return f"Country(name={self.name}, code={self.code})"


    def __str__(self):
        return f"{self.name}, {self.code}"


class Creator(Model):
    name = CharField(max_length=32, null=True, blank=True)
    surname = CharField(max_length=32, null=True, blank=True)
    date_of_birth = DateField(null=True, blank=True)
    date_of_death = DateField(null=True, blank=True)
    country_of_birth = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL, related_name='creators_born')
    country_of_death = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL, related_name='creators_died')
    biography = TextField(null=True, blank=True)


    class Meta:
        ordering = ['surname', 'name']


    def __repr__(self):
        return f"Creator(name={self.name} {self.surname})"


    def __str__(self):
        return f"{self.surname} {self.name}"


    def age(self):
        if self.date_of_birth:
            end_date = date.today()
            if self.date_of_death:
                end_date = self.date_of_death
            return (end_date.year - self.date_of_birth.year -
                    ((end_date.month, end_date.day) < (self.date_of_birth.month, self.date_of_birth.day)))
        return None


class Movie(Model):
    title_orig = CharField(max_length=150, null=False, blank=False)
    title_cz = CharField(max_length=150, null=True, blank=True)
    genres = ManyToManyField(Genre, blank=True, related_name='movies')
    countries = ManyToManyField(Country, blank=True, related_name='movies')
    actors = ManyToManyField(Creator, blank=True, related_name='as_actors')
    directors = ManyToManyField("viewer.Creator", blank=True, related_name='as_directors')  # druhá možnost napojení
    length = IntegerField(null=True, blank=True)
    released = IntegerField(null=True, blank=True)
    description = TextField(null=True, blank=True)
    rating = FloatField(null=True, blank=True)
    created_record = DateTimeField(auto_now_add=True)
    updated_record = DateTimeField(auto_now=True)


    class Meta:
        ordering = ['title_orig']


    def __repr__(self):
        return f"Movie(name={self.title_orig} ({self.title_cz}, released={self.released}))"


    def __str__(self):
        return f"{self.title_orig} / {self.title_cz} ({self.released})"
