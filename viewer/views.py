from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def hello(request):
    return HttpResponse('Hello, world!')


def hello2(request, s):
    return HttpResponse(f"Hello, {s} world!!")
