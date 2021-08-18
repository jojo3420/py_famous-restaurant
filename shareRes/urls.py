from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('restaurant/', views.RestaurantView.as_view(), name='restaurant'),
    path('category/', views.CategoryView.as_view(), name='category'),
    # path('detail/', views.detail),
]
