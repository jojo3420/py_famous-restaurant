from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    return render(request, 'shareRes/index.html')


def detail_page(request):
    return render(request, 'shareRes/restaurant_detail.html')


class RestaurantView(View):
    def get(self, request):
        id = request.GET['id']
        if id:
            # detail page
            return detail_page(request)
        # default page
        return render(request, 'shareRes/new_restaurant.html')

    def post(self, request):
        return HttpResponse('Restaurant post response')


class CategoryView(View):
    def get(self, request):
        return render(request, 'shareRes/new_category.html')

    def post(self, request):
        return HttpResponse('Category post response')
