from django.urls import path
from . import views

app_name= 'dashboard'

urlpatterns = [
    path('',views.dashboard,name='dashboard'),

    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/toggle/<int:product_id>/', views.toggle_product_status, name='toggle_product_status'),

    path('orders/', views.order_list, name='order_list'),
    path('orders/toggle/<int:order_id>/', views.toggle_order_completion, name='toggle_order_completion'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:user_id>/', views.customer_detail, name='customer_detail'),
    path('categories/', views.category_management, name='category_management'),

    # ADD THESE DEALS URLS
    path('deals/', views.deal_list, name='deal_list'),
    path('deals/<int:deal_id>/toggle/', views.toggle_deal_status, name='toggle_deal_status'),
    path('deals/<int:deal_id>/feature/', views.toggle_deal_featured, name='toggle_deal_featured'),
]

