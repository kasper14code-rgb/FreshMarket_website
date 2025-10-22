from .models import Cart

def cart_counter(request):
    cart_count = 0
    
    if request.user.is_authenticated:
        # For authenticated users - count items in database cart
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if cart:
            cart_count = cart.get_total_quantity()
    else:
        # For guests - count items in session cart
        session_cart = request.session.get('cart', {})
        cart_count = sum(session_cart.values())
    
    return {'cart_count': cart_count}