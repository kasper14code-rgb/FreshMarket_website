from django.urls import path
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
