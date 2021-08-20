from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('restaurant/', views.RestaurantView.as_view(), name='restaurant'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('detail/<int:restaurant_id>', views.RestaurantDetailView.as_view(), name='detail'),
    path('modify_detail/<int:restaurant_id>', views.modify_detail, name='modify_detail'),
    path('restaurant/remove/', views.remove_restaurant)
]
