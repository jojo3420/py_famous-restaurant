from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    return render(request, 'shareRes/index.html')


def new_restaurant(request):
    return render(request, 'shareRes/new_restaurant.html')


def detail(request):
    return render(request, 'shareRes/restaurant_detail.html')


def new_category(request):
    return render(request, 'shareRes/new_category.html')
