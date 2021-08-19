from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Category


# Create your views here.
def index(request):
    categories = Category.objects.all()
    data = {
        'categories': categories,
    }
    return render(request, 'shareRes/index.html', data)


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
        basic_category = Category.objects.filter(label='기본 그룹')
        categories = Category.objects.exclude(label='기본 그룹')
        data = {'basic_category': basic_category, 'categories': categories}
        return render(request, 'shareRes/new_category.html', data)

    def post(self, request):
        try:
            id = request.POST['id']
            if id:
                return self.remove(request, id)
        except KeyError:
            pass

        label = request.POST['categoryName']
        category = Category(label=label)
        category.save()
        return HttpResponseRedirect(reverse('category'))

    def remove(self, _request, id):
        category = Category.objects.get(id=id)
        if category:
            category.delete()
        return HttpResponseRedirect(reverse('category'))

    # def delete(self, request):
    #     return HttpResponse('delete request')
    #
    # def put(self, request):
    #     return HttpResponse('put request')
