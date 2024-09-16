from logging import getLogger

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.expressions import result
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from viewer.forms import CreatorForm, CreatorModelForm, MovieModelForm
from viewer.models import Movie, Creator, Genre

LOGGER = getLogger()


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
    return render(request, "creators.html", context)


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

# @login_required - používá se u funkce; u tříd používáme mixin, např: class CreatorUpdateView(LoginRequiredMixin, UpdateView)!
def creator(request, pk):
    if Creator.objects.filter(id=pk).exists():
        creator_ = Creator.objects.get(id=pk)
        return render(request, "creator.html", {'creator': creator_})
    return redirect('creators')


class CreatorCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    success_url = reverse_lazy('creators')
    permission_required = 'viewer.add_creator'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class CreatorUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    success_url = reverse_lazy('creators')
    model = Creator
    permission_required = 'viewer.change_creator'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a creator.')
        return super().form_invalid(form)


class CreatorDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Creator
    success_url = reverse_lazy('creators')
    permission_required = 'viewer.delete_creator'


class MovieCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')
    model = Movie

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a movie.')
        return super().form_invalid(form)


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('movies')




# TODO: Country - Create, Update, Delete
# TODO: Genre - Create, Update, Delete


def genres(request):
    genres_ = Genre.objects.all()
    context = {'genres': genres_}
    return render(request, 'genres.html', context)

def genre(request, pk):
    genre_ = Genre.objects.get(id=pk)
    movies_ = Movie.objects.filter(genres=genre_)
    context = {'genre': genre_, 'movies': movies_}
    return render(request, 'genre.html', context)
