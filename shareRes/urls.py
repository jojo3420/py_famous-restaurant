from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newRes/', views.new_restaurant),
    path('detail/', views.detail),
    path('newCategory/', views.new_category),
]
