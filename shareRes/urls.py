from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('category/delete/', views.delete_category),
    path('restaurant/', views.RestaurantView.as_view(), name='restaurant'),
    path('restaurant/<int:id>/', views.restaurant_detail_page, name='restaurant_detail_page'),
    path('restaurant/modify/<int:id>/', views.restaurant_modify_page),
    path('restaurant/modify/', views.restaurant_modify),
    path('restaurant/delete/', views.delete_restaurant),

]
