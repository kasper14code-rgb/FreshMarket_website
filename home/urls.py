from django.urls import path
from . import views
from reviews.views import add_review

app_name = 'home'  

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('cart/', views.cart, name='cart'),
    path('logout/', views.custom_logout, name='logout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('add-review/', add_review, name='add_review'), 
]
