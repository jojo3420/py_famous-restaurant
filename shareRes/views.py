from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from .models import Category, Restaurant


# Create your views here.
def index(request):
    categories = Category.objects.all()
    restaurants = Restaurant.objects.all()
    data = {
        'categories': categories,
        'restaurants': restaurants,
    }
    return render(request, 'shareRes/index.html', data)


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        data = {
            'categories': categories,
        }
        return render(request, 'shareRes/new_category.html', data)

    def post(self, request):
        query_dict = QueryDict(request.body)
        category = Category(label=query_dict['label'])
        if category:
            category.save()
        return HttpResponseRedirect(reverse('category'))


def delete_category(request):
    category_id = request.POST['category_id']
    if category_id:
        category = Category.objects.get(id=category_id)
        category.delete()
        return HttpResponseRedirect(reverse('category'))


class RestaurantView(View):
    def get(self, request):
        categories = Category.objects.all()
        data = {
            'categories': categories,
        }
        return render(request, 'shareRes/new_restaurant.html', data)

    def post(self, request):
        query_dict = QueryDict(request.body)
        category = Category.objects.get(id=query_dict['category_id'])
        restaurant = Restaurant(name=query_dict['name'], link=query_dict['link'], content=query_dict['content'],
                                keyword=query_dict['keyword'],
                                category=category)
        if restaurant:
            restaurant.save()
        return HttpResponseRedirect(reverse('index'))


def restaurant_detail_page(request, id):
    restaurant = Restaurant.objects.get(id=id)
    data = {
        'restaurant': restaurant,
    }
    return render(request, 'shareRes/restaurant_detail.html', data)


def restaurant_modify_page(request, id):
    restaurant = Restaurant.objects.get(id=id)
    categories = Category.objects.all()
    data = {
        'restaurant': restaurant,
        'categories': categories,
    }
    return render(request, 'shareRes/restaurant_modify.html', data)


def restaurant_modify(request):
    query_dict = QueryDict(request.body)
    restaurant_id = query_dict['restaurant_id']
    prev_restaurant = Restaurant.objects.get(id=restaurant_id)
    if prev_restaurant:
        prev_restaurant.name = query_dict['name']
        prev_restaurant.keyword = query_dict['keyword']
        prev_restaurant.link = query_dict['link']
        prev_restaurant.content = query_dict['content']
        category = Category.objects.get(id=query_dict['category_id'])
        prev_restaurant.category = category
        prev_restaurant.save()
        return HttpResponseRedirect(reverse('restaurant_detail_page', kwargs={'id': restaurant_id}))


def delete_restaurant(request):
    restaurant_id = request.POST['restaurant_id']
    if restaurant_id:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        restaurant.delete()
        return HttpResponseRedirect(reverse('index'))
