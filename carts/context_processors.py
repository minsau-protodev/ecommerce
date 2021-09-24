from .models import Cart, CartItem
from .views import _cart_id

def cart_counter(request):
    if 'admin' in request.path:
        return {}

    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
        cart_items = CartItem.objects.filter(cart=cart)
        
        total_items = 0
        for cart_item in cart_items:
            total_items += cart_item.quantity
    except Cart.DoesNotExist:
        total_items = 0

    return dict(total_items=total_items)