from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Deal


def deals_list(request):
    """Display all active deals"""
    now = timezone.now()
    
    # Get all active deals that are currently valid
    active_deals = Deal.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    ).prefetch_related('products')
    
    context = {
        'deals': active_deals,
        'page_title': 'Special Deals & Offers',
    }
    
    # ✅ Render the **list template**, not the detail template
    return render(request, 'deals/deals_list.html', context)


def deals_detail(request, deal_id):
    """Display single deal with products"""
    deal = get_object_or_404(Deal, id=deal_id, is_active=True)
    
    # Check if deal is still valid
    if not deal.is_valid():
        # Redirect to deals page if expired
        from django.shortcuts import redirect
        from django.contrib import messages
        messages.warning(request, 'This deal has expired.')
        return redirect('deals:deals_list')
    
    products = deal.products.filter(is_active=True)
    
    context = {
        'deal': deal,
        'products': products,
    }
    
    return render(request, 'deals/deals_detail.html', context)