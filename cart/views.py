from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from product.models import Product
from .models import Cart, CartItem

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
    product = get_object_or_404(Product, id=product_id)

    # Get quantity from POST (default to 1 if not provided)
    quantity = int(request.POST.get('quantity', 1))

    # If user is authenticated, use the database cart
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Update the quantity if already in cart
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f"Added {quantity} {product.name} to cart.")

    # For guests (not logged in), store in session
    else:
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart
        messages.success(request, f"Added {quantity} {product.name} to cart.")

    return redirect('cart:cart_detail')

def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        # For authenticated users - get cart first, then cart item
        cart = get_object_or_404(Cart, user=request.user, is_active=True)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    else:
        # For guests - remove from session cart
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            product_name = Product.objects.get(id=product_id).name
            del cart[str(product_id)]
            request.session['cart'] = cart
            messages.success(request, f"{product_name} removed from cart.")
        else:
            messages.error(request, "Item not found in cart.")
    
    return redirect('cart:cart_detail')

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if request.user.is_authenticated:
            # For authenticated users
            cart = get_object_or_404(Cart, user=request.user, is_active=True)
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, "Cart updated.")
            else:
                cart_item.delete()
                messages.success(request, "Item removed from cart.")
        else:
            # For guests - update session cart
            cart = request.session.get('cart', {})
            if quantity > 0:
                cart[str(product_id)] = quantity
                messages.success(request, "Cart updated.")
            else:
                # Remove if quantity is 0 or less
                if str(product_id) in cart:
                    product_name = Product.objects.get(id=product_id).name
                    del cart[str(product_id)]
                    messages.success(request, f"{product_name} removed from cart.")
            request.session['cart'] = cart
    
    return redirect('cart:cart_detail')

def cart_detail(request):
    if request.user.is_authenticated:
        # Get active cart for the logged-in user
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            # Calculate total for authenticated users
            total = cart.get_total_price()
        else:
            cart_items = CartItem.objects.none()
            total = 0
    else:
        # For guests, use session cart
        session_cart = request.session.get('cart', {})
        cart_items = []
        for product_id, quantity in session_cart.items():
            product = get_object_or_404(Product, id=product_id)
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,  # Changed from 'item_total' to 'total' for template consistency
            })
        total = sum(item['total'] for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart_detail.html', context)