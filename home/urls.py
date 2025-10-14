from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/',auth_views.LogoutView.as_view(next_page = 'home:index'),name ='logout'),
    path('cart/', views.cart, name='cart'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
