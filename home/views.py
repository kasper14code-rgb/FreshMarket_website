from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from product.models import Product, Category
from .models import Testimonial

@login_required
def my_orders(request):
    # Fetch orders for the logged-in user
    orders = request.user.orders.all()  # Adjust depending on your Order model
    return render(request, 'home/my_orders.html', {'orders': orders})


def index(request):
    # Get bestsellers and active products
    bestsellers = Product.objects.filter(is_bestseller=True, is_active=True)[:5]
    products = Product.objects.filter(is_active=True)[:5]
    
    # Get testimonials and categories
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    categories = Category.objects.all()

    # Combine into one clean context
    context = {
        'bestsellers': bestsellers,
        'products': products,
        'testimonials': testimonials,
        'categories': categories,
    }

    # Render homepage
    return render(request, 'home/index.html', context)


def login(request):
    return render(request, 'home/login.html')


def cart(request):
    return render(request, 'home/cart.html')
