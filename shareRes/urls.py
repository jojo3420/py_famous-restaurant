from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('restaurant/', views.RestaurantView.as_view()),
    path('category/', views.CategoryView.as_view()),
    # path('detail/', views.detail),
]
