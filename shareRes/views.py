from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.urls import reverse
from .models import Category, Restaurant


# Create your views here.
def index(request):
    """
    메인 페이지
    :param request:
    :return:
    """
    categories = Category.objects.all()
    restaurants = Restaurant.objects.all()
    data = {
        'categories': categories,
        'restaurants': restaurants,
    }
    return render(request, 'shareRes/index.html', data)


def modify_detail(request, restaurant_id):
    """
    맛집(restaurant) 수정 페이지(GET)
    :param request:
    :param restaurant_id:
    :return:
    """
    categories = Category.objects.all()
    restaurant = Restaurant.objects.get(id=restaurant_id)
    data = {'categories': categories, 'restaurant': restaurant}
    return render(request, 'shareRes/modify_restaurant.html', data)


def remove_restaurant(request):
    """
    맛집(restaurant) 제거
    :param request:
    :return:
    """
    restaurant_id = request.POST['restaurant_id']
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if restaurant:
        restaurant.delete()
    return HttpResponseRedirect(reverse('index'))


class RestaurantView(View):
    def get(self, request):
        """
        맛집(레스토랑) 등록하기 페이지
        :param request:
        :return:
        """
        categories = Category.objects.all()
        data = {'categories': categories}
        return render(request, 'shareRes/new_restaurant.html', data)

    def post(self, request):
        """
        맛집(레스토랑) 신규 등록
        :param request:
        :return:
        """
        query_dict = QueryDict(request.body)
        if query_dict:
            category = Category.objects.get(id=query_dict['category'])
            Restaurant(name=query_dict['name'], link=query_dict['link'], content=query_dict['content'],
                       keyword=query_dict['keyword'], category=category).save()

        return HttpResponseRedirect(reverse('index'))


class CategoryView(View):
    def get(self, request):
        """
        카테고리 등록(Register) 페이지
        :param request:
        :return:
        """
        basic_category = Category.objects.filter(label='기본 그룹')
        categories = Category.objects.exclude(label='기본 그룹')
        data = {'basic_category': basic_category, 'categories': categories}
        return render(request, 'shareRes/new_category.html', data)

    def post(self, request):
        """
        카테고리 신규 등록 및 카테고리 삭제
        파라미터로 id가 있을 경우 삭제, id 가없으면서 categoryName 파라미터가 있으면 신규등록
        :param request: id: 삭제할 카테고리 아이디
        :return:
        """
        try:
            category_id = request.POST['id']
            if category_id:
                return self.remove(request, category_id)
        except KeyError:
            pass
        label = request.POST['categoryName']
        category = Category(label=label)
        category.save()
        return HttpResponseRedirect(reverse('category'))

    def remove(self, _request, category_id):
        """
        (임시) 카테고리 삭제
        함수명 변경 필요 DELETE method 맞게 수정 => delete
        :param _request:
        :param id:
        :return:
        """
        category = Category.objects.get(id=category_id)
        if category:
            category.delete()
        return HttpResponseRedirect(reverse('category'))


class RestaurantDetailView(View):
    def get(self, request, restaurant_id):
        """
         레스토랑(맛집) 상세 페이지
        :param request:
        :param id:
        :return:
        """
        restaurant = Restaurant.objects.get(id=restaurant_id)
        data = {'restaurant': restaurant}
        return render(request, 'shareRes/restaurant_detail.html', data)

    def post(self, request, restaurant_id):
        """
        맛집(Restaurant) 상세 정보 수정
          상호명, link, 상세내용, 키워드, 카테고리 변경
        :param request:
        :return:
        """
        query_dict = QueryDict(request.body)
        prev_restaurant = Restaurant.objects.get(id=restaurant_id)
        if prev_restaurant:
            prev_restaurant.name = query_dict['name']
            prev_restaurant.link = query_dict['link']
            prev_restaurant.content = query_dict['content']
            prev_restaurant.keyword = query_dict['keyword']
            prev_restaurant.category = Category.objects.get(id=query_dict['category'])
            prev_restaurant.save()
        return HttpResponseRedirect(reverse('detail', kwargs={'restaurant_id': restaurant_id}))
