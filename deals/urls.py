from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    path('', views.deals_list, name='deals_list'),
    path('<int:deal_id>/', views.deals_detail, name='deals_detail'),
]