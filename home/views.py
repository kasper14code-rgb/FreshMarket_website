from django.contrib.auth.decorators import login_required
from django.shortcuts import render ,redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
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
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')  # change 'index' to wherever you want to send logged-in users
    else:
        form = AuthenticationForm()

    return render(request, 'home/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:login')  # Redirect to login page after signup
    else:
        form = CustomUserCreationForm()

    return render(request, 'home/signup.html', {'form': form})

def cart(request):
    return render(request, 'home/cart.html')

def logout_view(request):
    logout(request)
    return redirect('index')
