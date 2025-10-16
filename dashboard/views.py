from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from product.models import Product, Category, Order
from reviews.models import Review
from cart.models import Cart, CartItem
from .forms import ProductForm, CategoryForm
from deals.models import Deal

def staff_required(user):
    return user.is_staff

@staff_member_required
def dashboard(request):
    # Calculate real statistics from your models
    total_orders = Order.objects.count()
    
    # Calculate revenue from completed orders
    completed_orders = Order.objects.filter(is_completed=True)
    total_revenue = sum(order.product.price * order.quantity for order in completed_orders)
    
    active_customers = User.objects.filter(is_active=True).count()
    total_products = Product.objects.filter(is_active=True).count()
    
    # Calculate growth (orders in last 30 days vs previous 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    sixty_days_ago = timezone.now() - timedelta(days=60)
    
    recent_orders_count = Order.objects.filter(ordered_at__gte=thirty_days_ago).count()
    previous_orders_count = Order.objects.filter(
        ordered_at__gte=sixty_days_ago, 
        ordered_at__lt=thirty_days_ago
    ).count()
    
    if previous_orders_count > 0:
        growth_rate = ((recent_orders_count - previous_orders_count) / previous_orders_count) * 100
    else:
        growth_rate = 100 if recent_orders_count > 0 else 0

    now = timezone.now()
    active_deals = Deal.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    )
    total_deals = Deal.objects.count()

    # Get recent data
    recent_orders = Order.objects.select_related('user', 'product').order_by('-ordered_at')[:5]
    low_stock_products = Product.objects.filter(stock__lt=10, is_active=True)[:5]
    recent_reviews = Review.objects.select_related('product').filter(is_approved=True).order_by('-created_at')[:5]
    bestsellers = Product.objects.filter(is_bestseller=True, is_active=True)[:4]
    categories = Category.objects.all()

    context = {
        'page_title': 'Dashboard Overview',
        'stats': {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'active_customers': active_customers,
            'total_products': total_products,
            'growth_rate': round(growth_rate, 1),
            'total_deals': total_deals,  # ADD THIS
            'active_deals_count': active_deals.count(),
        },
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'recent_reviews': recent_reviews,
        'bestsellers': bestsellers,
        'categories': categories,
        'recent_products': Product.objects.filter(is_active=True).order_by('-created_at')[:5],
        'recent_products': Product.objects.filter(is_active=True).order_by('-created_at')[:5],
        'active_deals': active_deals[:5], 
    }
    return render(request, 'dashboard/dashboard.html', context)
@staff_member_required
def deal_list(request):
    deals = Deal.objects.all().order_by('-created_at')
    
    # Filtering
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        deals = deals.filter(is_active=True)
    elif status_filter == 'featured':
        deals = deals.filter(is_featured=True)
    elif status_filter == 'expired':
        deals = deals.filter(end_date__lt=timezone.now())
    
    return render(request, 'dashboard/deal_list.html', {
        'deals': deals,
        'page_title': 'Deals Management',
        'status_filter': status_filter,
    })

@staff_member_required
def toggle_deal_status(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    deal.is_active = not deal.is_active
    deal.save()
    
    action = "activated" if deal.is_active else "deactivated"
    messages.success(request, f'Deal "{deal.title}" {action} successfully!')
    return redirect('dashboard:deal_list')

@staff_member_required
def toggle_deal_featured(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    deal.is_featured = not deal.is_featured
    deal.save()
    
    action = "featured" if deal.is_featured else "unfeatured"
    messages.success(request, f'Deal "{deal.title}" {action} successfully!')
    return redirect('dashboard:deal_list')

# Product Management Views
@staff_member_required
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/product_list.html', {
        'products': products,
        'page_title': 'Product Management'
    })

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
    
    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'page_title': 'Add New Product'
    })
@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'page_title': f'Edit {product.name}',
        'product': product
    })
@staff_member_required
def toggle_product_status(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_active = not product.is_active
    product.save()
    
    action = "activated" if product.is_active else "deactivated"
    messages.success(request, f'Product "{product.name}" {action} successfully!')
    return redirect('dashboard:product_list')

# Order Management Views
@staff_member_required
def order_list(request):
    orders = Order.objects.select_related('user', 'product').order_by('-ordered_at')
    
    # Filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        if status_filter == 'completed':
            orders = orders.filter(is_completed=True)
        elif status_filter == 'pending':
            orders = orders.filter(is_completed=False)
    
    return render(request, 'dashboard/order_list.html', {
        'orders': orders,
        'page_title': 'Order Management',
        'status_filter': status_filter,
    })

@staff_member_required
def toggle_order_completion(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_completed = not order.is_completed
    order.save()
    
    status = "completed" if order.is_completed else "pending"
    messages.success(request, f'Order #{order.id} marked as {status}!')
    return redirect('dashboard:order_list')

# Customer Management Views
@staff_member_required
def customer_list(request):
    customers = User.objects.filter(is_active=True).annotate(
        order_count=Count('orders'),
        total_spent=Sum('orders__product__price')
    ).order_by('-date_joined')
    
    return render(request, 'dashboard/customer_list.html', {
        'customers': customers,
        'page_title': 'Customer Management'
    })

@staff_member_required
def customer_detail(request, user_id):
    customer = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(user=customer).order_by('-ordered_at')
    recent_reviews = Review.objects.filter(email=customer.email).order_by('-created_at')[:5]
    
    return render(request, 'dashboard/customer_detail.html', {
        'customer': customer,
        'orders': orders,
        'recent_reviews': recent_reviews,
        'page_title': f'Customer: {customer.get_full_name() or customer.username}'
    })

# Category Management
@staff_member_required
def category_management(request):
    categories = Category.objects.all().order_by('name')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" added successfully!')
            return redirect('dashboard:category_management')
    else:
        form = CategoryForm()
    
    return render(request, 'dashboard/category_management.html', {
        'categories': categories,
        'form': form,
        'page_title': 'Category Management'
    })