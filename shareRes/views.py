from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
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


class RestaurantView(View):
    def get(self, request):
        try:
            id = request.GET['id']
            print(f'id: {id}')
            if id:
                # detail page
                return detail_page(request, id)
        except MultiValueDictKeyError:
            pass
        categories = Category.objects.all()
        data = {'categories': categories}
        return render(request, 'shareRes/new_restaurant.html', data)

    def post(self, request):
        _token, category_id, name, link, content, keyword = dict(request.POST).values()
        print(category_id, name, link, content, keyword)
        if category_id and name:
            category = Category.objects.get(id=category_id[0])
            Restaurant(name=name[0], link=link[0], content=content[0], keyword=keyword[0], category=category).save()

        return HttpResponseRedirect(reverse('index'))


class CategoryView(View):
    def get(self, request):
        """
        카테고리 추가 페이지
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
        TODO: DELETE method 수정할 방법 찾을 때 까지 임시 적용
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

    # def delete(self, request):
    #     return HttpResponse('delete request')
    #
    # def put(self, request):
    #     return HttpResponse('put request')


class RestaurantDetailView(View):
    def get(self, request, restaurant_id):
        """
         레스토랑(맛집) 상세 페이지
        :param request:
        :param id:
        :return:
        """
        print('restaurant_id:', restaurant_id)
        restaurant = Restaurant.objects.get(id=restaurant_id)
        data = {
            'restaurant': restaurant,
        }
        return render(request, 'shareRes/restaurant_detail.html', data)

    def post(self, request):
        return HttpResponse('detail post')

    def delete(self, request):
        return HttpResponse('detail delete')

    def put(self, request):
        return HttpResponse('detail put')
