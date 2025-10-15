from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from product.models import Product, Category
from reviews.models import Review
from django.contrib import messages
from django.db.models import Avg

@login_required
def my_orders(request):
    # Fetch orders for the logged-in user
    orders = request.user.orders.all()  # Adjust depending on your Order model
    return render(request, 'home/my_orders.html', {'orders': orders})


def index(request):
    # Get bestsellers and active products
    bestsellers = Product.objects.filter(is_bestseller=True, is_active=True)[:5]
    products = Product.objects.filter(is_active=True)[:5]
    
    # Get all approved reviews first (without slicing)
    approved_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    
    # Calculate review statistics
    total_reviews = approved_reviews.count()
    if total_reviews > 0:
        average_rating = approved_reviews.aggregate(Avg('rating'))['rating__avg']
        positive_reviews = approved_reviews.filter(rating__gte=4).count()
        positive_percentage = round((positive_reviews / total_reviews) * 100)
    else:
        average_rating = 0
        positive_percentage = 0
    
    # Now slice for display (only the first 6 reviews)
    reviews = approved_reviews[:6]
    
    categories = Category.objects.all()

    # Combine into one clean context
    context = {
        'bestsellers': bestsellers,
        'products': products,
        'reviews': reviews,
        'categories': categories,
        'total_reviews': total_reviews,
        'average_rating': round(average_rating, 1) if average_rating else 0,
        'positive_percentage': positive_percentage,
    }

    # Render homepage
    return render(request, 'home/index.html', context)



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home:index')  # change 'index' to wherever you want to send logged-in users
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
    return render(request, 'cart/cart_detail.html')

def custom_logout(request):
    logout(request)
    return redirect('home:index')