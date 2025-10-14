from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/', views.add_review, name='add_review'),
    path('', views.review_list, name='review_list'),  # For viewing all approved reviews
]