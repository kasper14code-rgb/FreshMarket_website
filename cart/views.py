from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Product

def cart_view(request):
    # Get cart from session (or empty dict)
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart:cart')

def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
    cart_item.delete()
    return redirect('cart:cart_detail') 

# Update quantity of a cart item
def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    # Calculate line totals for each item
    for item in cart_items:
        item.total = item.product.price * item.quantity

    # Calculate cart total
    total = sum(item.total for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart_detail.html', context)