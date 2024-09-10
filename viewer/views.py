from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from viewer.models import Movie, Creator, Genre


def home(request):
    return render(request, 'home.html')


def movies(request):
    movies_ = Movie.objects.all()
    context = {'movies': movies_}
    return render(request, 'movies.html', context)


def movie(request, pk):
    if Movie.objects.filter(id=pk).exists():
        movie_ = Movie.objects.get(id=pk)
        context = {'movie': movie_}
        return render(request, 'movie.html', context)
    return movies(request)


# Class-Based View (CBV)
## View class
class MoviesView(View):
    def get(self, request):
        movies_ = Movie.objects.all()
        context = {'movies': movies_}
        return render(request, "movies.html", context)


## TemplateView class
class MoviesTemplateView(TemplateView):
    template_name = "movies.html"
    extra_context = {'movies': Movie.objects.all()}


## ListView class
class MoviesListView(ListView):
    template_name = "movies.html"
    model = Movie
    # pozor: do template se posílají data jako 'object_list'
    # můžeme to přejmenovat:
    context_object_name = 'movies'

    #pokud bych potřeboval jen nějakou podmnožinu dat (filtr), lze předefinovat context data:
    # pokud chci pouze Krimi filmy:
    """def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        crime_genre = Genre.objects.get(name="Krimi")
        crime_movies = Movie.objects.filter(genres=crime_genre)
        context['movies'] = crime_movies
        return context"""


def creators(request):
    creators_ = Creator.objects.all()
    context = {'creators': creators_}
    return render(request, 'creators.html', context)


def creator(request,pk):
    if Creator.objects.filter(id=pk).exists():
        creator_ = Creator.objects.get(id=pk)
        context = {'creator': creator_}
        return render(request, 'creator.html', context)
    return creators(request)


class CreatorsView(View):
    def get(self, request):
        creators_ = Creator.objects.all()
        context = {'creators': creators_}
        return render(request, "creators.html", context)


class CreatorsTemplateView(TemplateView):
    template_name = "creators.html"
    extra_context = {'creators': Creator.objects.all()}


class CreatorsListView(ListView):
    template_name = "creators.html"
    model = Creator
    context_object_name = 'creators'


def genres(request):
    genres_ = Genre.objects.all()
    context = {'genres': genres_}
    return render(request, 'genres.html', context)

def genre(request, pk):
    genre_ = Genre.objects.get(id=pk)
    movies_ = Movie.objects.filter(genres=genre_)
    context = {'genre': genre_, 'movies': movies_}
    return render(request, 'genre.html', context)