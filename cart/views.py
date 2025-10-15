from django.shortcuts import render, redirect, get_object_or_404
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

    # For guests (not logged in), store in session
    else:
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart

    return redirect('cart:cart_detail')

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
    if request.user.is_authenticated:
        # Get active cart for the logged-in user
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
        else:
            cart_items = CartItem.objects.none()
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
                'item_total': item_total,
            })

    # Calculate totals
    if request.user.is_authenticated:
        for item in cart_items:
            item.total = item.product.price * item.quantity
        total = sum(item.total for item in cart_items)
    else:
        total = sum(item['item_total'] for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart_detail.html', context)
