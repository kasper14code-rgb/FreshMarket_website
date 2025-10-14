from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg
from .models import Product, Category
from reviews.models import Review

def product_list(request):
    products = Product.objects.filter(is_active=True)  # ✅ Always defined at the start
    categories = Category.objects.all()

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug and category_slug != "all":
        products = products.filter(category__slug=category_slug)

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Sorting
    sort_by = request.GET.get('sort', 'default')
    if sort_by == 'price-asc':
        products = products.order_by('price')
    elif sort_by == 'price-desc':
        products = products.order_by('-price')
    elif sort_by == 'name-asc':
        products = products.order_by('name')
    elif sort_by == 'name-desc':
        products = products.order_by('-name')

    context = {
        'products': products,          # ✅ Safe to use now
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'product/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = Review.objects.filter(product=product, is_approved=True).order_by('-created_at')
    
    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': product.get_average_rating(),
        'review_count': product.get_review_count(),
    }
    return render(request, 'product/product_detail.html', context)